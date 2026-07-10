#!/usr/bin/env python3
"""Create WeChat Official Account drafts. This client never publishes articles."""
import argparse
import json
import mimetypes
import os
import uuid
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API = "https://api.weixin.qq.com/cgi-bin"

def output(data, code=0):
    print(json.dumps(data, ensure_ascii=False))
    raise SystemExit(code)

def require_credentials():
    appid, secret = os.getenv("WECHAT_APPID"), os.getenv("WECHAT_SECRET")
    missing = [key for key, value in (("WECHAT_APPID", appid), ("WECHAT_SECRET", secret)) if not value]
    if missing:
        output({"ok": False, "error": "Missing environment variables", "missing": missing}, 1)
    return appid, secret

def json_request(url, payload=None):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
    try:
        with urlopen(Request(url, data=data, headers={"Content-Type": "application/json; charset=utf-8"}), timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError) as error:
        output({"ok": False, "error": str(error)}, 1)
    if result.get("errcode", 0):
        output({"ok": False, "error": result.get("errmsg"), "errcode": result.get("errcode")}, 1)
    return result

def token():
    appid, secret = require_credentials()
    return json_request(f"{API}/token?" + urlencode({"grant_type": "client_credential", "appid": appid, "secret": secret}))["access_token"]

def multipart(path):
    file_path = Path(path)
    boundary = "----Codex" + uuid.uuid4().hex
    mime = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    body = b"--" + boundary.encode() + b"\r\n"
    body += f'Content-Disposition: form-data; name="media"; filename="{file_path.name}"\r\n'.encode()
    body += f"Content-Type: {mime}\r\n\r\n".encode() + file_path.read_bytes() + b"\r\n"
    body += b"--" + boundary.encode() + b"--\r\n"
    return body, boundary

def upload_cover(path):
    body, boundary = multipart(path)
    url = f"{API}/material/add_material?access_token={token()}&type=image"
    try:
        with urlopen(Request(url, data=body, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}), timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError) as error:
        output({"ok": False, "error": str(error)}, 1)
    if result.get("errcode", 0):
        output({"ok": False, "error": result.get("errmsg"), "errcode": result.get("errcode")}, 1)
    output({"ok": True, "media_id": result.get("media_id"), "url": result.get("url")})

def create_draft(path):
    article = json.loads(Path(path).read_text(encoding="utf-8"))
    missing = [key for key in ("title", "content", "thumb_media_id") if not article.get(key)]
    if missing:
        output({"ok": False, "error": "Article JSON missing fields", "missing": missing}, 1)
    allowed = {"title", "author", "digest", "content", "content_source_url", "thumb_media_id", "need_open_comment", "only_fans_can_comment"}
    result = json_request(f"{API}/draft/add?access_token={token()}", {"articles": [{key: value for key, value in article.items() if key in allowed}]})
    output({"ok": True, "status": "draft_created", "media_id": result.get("media_id")})

parser = argparse.ArgumentParser(description="WeChat draft-only client")
sub = parser.add_subparsers(dest="command", required=True)
sub.add_parser("doctor")
cover = sub.add_parser("upload-cover")
cover.add_argument("file")
draft = sub.add_parser("create-draft")
draft.add_argument("article_json")
args = parser.parse_args()

if args.command == "doctor":
    missing = [key for key in ("WECHAT_APPID", "WECHAT_SECRET") if not os.getenv(key)]
    output({"ok": not missing, "draft_supported": not missing, "publish_supported": False, "missing": missing})
elif args.command == "upload-cover":
    upload_cover(args.file)
else:
    create_draft(args.article_json)
