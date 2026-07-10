# WeChat Draft Skill

一个面向 Codex 的微信公众平台草稿箱 Skill：通过微信官方接口上传封面图、创建图文草稿，并刻意不包含群发或发布能力。

> 适用于已经拥有已认证公众号、开发者凭据和 API 白名单权限的运营者或开发者。

## 能做什么

- 检查本机是否已配置微信开发者凭据；
- 上传文章封面图并取得 `thumb_media_id`；
- 将准备好的 HTML 文章创建到公众号草稿箱；
- 只创建草稿，**不会群发、发布或删除公众号内容**。

## 安装到 Codex

```powershell
git clone https://github.com/hxy180/wechat-draft-skill.git "$env:USERPROFILE\.codex\skills\wechat-draft-skill"
```

重启 Codex 后，它会自动发现该 Skill。也可以直接使用当前仓库中的脚本。

## 前置条件

1. 已开通并完成认证的微信公众号；
2. 已启用开发者模式，并取得 AppID 与 AppSecret；
3. 已将当前网络的公网 IP 加入公众号开发者 API 白名单；
4. 本机已安装 Python 3.9 或更高版本。

不要把 AppSecret 写入文章、配置文件或提交到 Git 仓库。

## 配置凭据

在 PowerShell 中设置当前 Windows 用户的环境变量：

```powershell
[Environment]::SetEnvironmentVariable('WECHAT_APPID', '<你的 AppID>', 'User')
[Environment]::SetEnvironmentVariable('WECHAT_SECRET', '<你的 AppSecret>', 'User')
```

关闭并重新打开终端后，进入仓库目录执行：

```powershell
python scripts/wechat_draft.py doctor
```

预期会得到类似结果：

```json
{"ok": true, "draft_supported": true, "publish_supported": false, "missing": []}
```

## 创建一篇草稿

### 1. 准备封面图

封面图请使用你有权使用的 JPG 或 PNG 文件。

```powershell
python scripts/wechat_draft.py upload-cover .\cover.jpg
```

记录返回结果中的 `media_id`。

### 2. 准备文章 JSON

创建 `article.json`：

```json
{
  "title": "示例文章标题",
  "author": "",
  "digest": "一段简短摘要",
  "content": "<p>这里放已排版的 HTML 正文。</p>",
  "content_source_url": "https://example.com",
  "thumb_media_id": "上一步返回的 media_id",
  "need_open_comment": 0,
  "only_fans_can_comment": 0
}
```

其中 `title`、`content` 与 `thumb_media_id` 必填。`content` 应为完整、可信的 HTML 内容。

### 3. 写入草稿箱

```powershell
python scripts/wechat_draft.py create-draft .\article.json
```

脚本返回 `draft_created` 与草稿 `media_id` 即表示创建成功。请前往公众号后台完成预览、校对和后续发布操作。

## 与公众号写作工作流配合

建议顺序：先完成选题、写作和公众号 HTML 排版；核对图片版权与链接；再使用本 Skill 上传封面并创建草稿。草稿创建前，确认目标公众号账号与文章标题。

## 安全边界

- 本仓库不会调用群发、发布或删除接口；
- 请勿在 Issue、日志、截图或代码中泄露 AppSecret；
- API 白名单与权限由微信公众号后台控制；
- 创建草稿后仍应由人工在后台检查排版、封面、来源和合规性。

## 开发与验证

```powershell
python scripts/wechat_draft.py doctor
python C:\Users\侯晓宇\.codex\skills\.system\skill-creator\scripts\quick_validate.py .
```

详见 [CONTRIBUTING.md](CONTRIBUTING.md) 与 [SECURITY.md](SECURITY.md)。

## 许可证

本项目采用 [MIT License](LICENSE)。
