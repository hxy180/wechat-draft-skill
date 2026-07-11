---
name: wechat-draft-skill
description: Create WeChat Official Account article drafts through the official API. Use when a user asks to check WeChat draft credentials, upload an article cover, or create a WeChat draft from prepared HTML. Never use for mass sending or publishing.
---

# WeChat Draft Skill

Use `scripts/wechat_draft.py` to create a draft through the official WeChat Official Account API.

## Safety

- Create drafts only. Never call mass-send or publish APIs.
- Before uploading a cover or creating a draft, confirm the target account and article title in the current turn.
- Run `doctor` before any network action. If credentials are missing, stop and tell the user how to configure them locally. Never request secrets in chat.
- Require a verified cover `media_id` and prepared HTML before creating a draft.

## Commands

```powershell
python scripts/wechat_draft.py doctor
python scripts/wechat_draft.py upload-cover cover.jpg
python scripts/wechat_draft.py create-draft article.json
python scripts/wechat_draft.py update-draft update.json
```

`article.json` must include `title`, `content`, and `thumb_media_id`. It may include `author`, `digest`, `content_source_url`, `need_open_comment`, and `only_fans_can_comment`.

Use `update-draft` only to correct an existing draft after confirming the target draft and article title in the current turn. Its JSON must include `media_id`, `index`, and an `article` object with the same required fields. Upload every inline article image to permanent WeChat material first, then replace external image URLs in `content` with the returned WeChat material URLs before creating or updating a draft.

## Local credentials

Set credentials in the local user environment, restart the terminal, then run `doctor` again:

```powershell
[Environment]::SetEnvironmentVariable('WECHAT_APPID', '<your-appid>', 'User')
[Environment]::SetEnvironmentVariable('WECHAT_SECRET', '<your-secret>', 'User')
```

Add the machine's public outbound IP to the WeChat Official Account API whitelist. Do not create a draft until both credential and whitelist checks are complete.
