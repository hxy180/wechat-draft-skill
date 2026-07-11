# WeChat Draft Agent Instructions

Use this repository with any AI agent that can read project instructions and run local Python commands.

## Goal

Create or update a WeChat Official Account **draft only** through the official API. Never mass-send, publish, delete, or modify published content.

## Required safety sequence

1. Confirm the target WeChat account and article title in the current conversation before any upload or draft mutation.
2. Run `python scripts/wechat_draft.py doctor` before network actions.
3. Read `WECHAT_APPID` and `WECHAT_SECRET` only from local environment variables. Never ask for, print, log, commit, or transmit secrets in chat.
4. Require a local cover image and prepared HTML before creating a draft.
5. Upload every inline article image with `upload-image`; replace external `<img src>` URLs with the returned WeChat material URL before creating or updating a draft.
6. After a successful draft creation or update, report that it remains unpublished and ask the user to preview it in the WeChat backend.

## Commands

```bash
python scripts/wechat_draft.py doctor
python scripts/wechat_draft.py upload-cover cover.png
python scripts/wechat_draft.py upload-image image.png
python scripts/wechat_draft.py create-draft article.json
python scripts/wechat_draft.py update-draft update.json
```

`create-draft` requires `title`, `content`, and `thumb_media_id`. `update-draft` requires the existing draft `media_id`, article `index`, and a complete `article` object.
