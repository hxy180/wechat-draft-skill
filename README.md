# WeChat Draft Skill

> 把已写好的公众号 HTML，安全地送进微信公众平台草稿箱。

`wechat-draft-skill` 是一个可被 [Codex](https://openai.com/codex/) 发现和调用的 Skill，也可以作为一个零依赖的 Python 命令行工具单独使用。它通过微信公众平台官方接口完成两件事：上传文章封面图、创建图文草稿。

它**只创建草稿**。仓库中没有群发、发布、删除或修改已发布文章的实现，因此你仍然可以在公众号后台人工检查内容后再决定是否发布。

## 适合谁

- 用 Codex 写公众号文章，希望最后一步自动进入草稿箱的内容创作者；
- 已有公众号后台权限，想用脚本把 HTML 文章交给编辑审核的团队；
- 希望把“写作 → 排版 → 草稿箱”拆成可复用流程的开发者。

如果你没有公众号的 AppID、AppSecret 或 API 白名单权限，这个 Skill 仍能安装和阅读，但无法向草稿箱写入内容。

## 功能一览

| 功能 | 命令 | 结果 |
| --- | --- | --- |
| 检查环境 | `doctor` | 确认本机是否已配置凭据 |
| 上传封面 | `upload-cover` | 返回可用于草稿的 `media_id` |
| 创建草稿 | `create-draft` | 返回公众号草稿的 `media_id` |
| 群发 / 发布 | 不支持 | 始终保留人工审核环节 |

## 30 秒快速开始

### 1. 安装

在 PowerShell 中执行：

```powershell
git clone https://github.com/hxy180/wechat-draft-skill.git "$env:USERPROFILE\.codex\skills\wechat-draft-skill"
cd "$env:USERPROFILE\.codex\skills\wechat-draft-skill"
```

重启 Codex 后，它会自动发现这个 Skill。若只想以命令行方式使用，不需要重启，保持在仓库目录即可。

> Windows 默认安装位置为 `C:\Users\你的用户名\.codex\skills\wechat-draft-skill`。macOS / Linux 可克隆到 `~/.codex/skills/wechat-draft-skill`。

### 2. 配置公众号凭据

前往公众号后台的开发者设置，取得 AppID 与 AppSecret；将你当前网络的公网 IP 加入 API 白名单。随后设置**当前用户**环境变量：

```powershell
[Environment]::SetEnvironmentVariable('WECHAT_APPID', '<你的 AppID>', 'User')
[Environment]::SetEnvironmentVariable('WECHAT_SECRET', '<你的 AppSecret>', 'User')
```

关闭并重新打开终端，然后运行：

```powershell
python scripts/wechat_draft.py doctor
```

成功时会输出：

```json
{"ok": true, "draft_supported": true, "publish_supported": false, "missing": []}
```

如果输出含有 `missing`，说明新终端还没有读到环境变量；不要把密钥粘贴到 Issue、聊天记录或 JSON 文件中。

### 3. 上传封面并创建草稿

```powershell
# 上传有使用权的 JPG 或 PNG 封面图
python scripts/wechat_draft.py upload-cover .\cover.jpg

# 将上一步返回的 media_id 填入 article.json 后创建草稿
python scripts/wechat_draft.py create-draft .\article.json
```

看到 `"status": "draft_created"` 就表示草稿已进入目标公众号后台。打开公众号后台检查排版、封面、来源和错别字，再进行后续操作。

## 完整使用教程

### 第一步：准备文章 HTML

`content` 字段接收 HTML。你可以来自 Codex 生成的文章、公众号排版工具导出的 HTML，或自行编写的简单标签。先在本地浏览器或公众号编辑器中检查最终效果。

最小 HTML 示例：

```html
<h2>AI 观察：一个具体变化</h2>
<p>这是正文第一段。</p>
<p><strong>这句话需要强调。</strong></p>
```

### 第二步：上传封面

封面图必须是你有权使用的本地文件。执行：

```powershell
python scripts/wechat_draft.py upload-cover .\cover.jpg
```

成功输出中的 `media_id` 是创建草稿必须的封面标识。请复制它，但不要把它当作公开链接使用。

### 第三步：建立文章描述文件

复制 [examples/article.example.json](examples/article.example.json) 为 `article.json`，然后替换标题、摘要、正文和 `thumb_media_id`：

```powershell
Copy-Item .\examples\article.example.json .\article.json
notepad .\article.json
```

字段说明：

| 字段 | 是否必填 | 说明 |
| --- | --- | --- |
| `title` | 是 | 文章标题 |
| `content` | 是 | HTML 正文 |
| `thumb_media_id` | 是 | 上传封面后得到的 `media_id` |
| `author` | 否 | 文章作者 |
| `digest` | 否 | 摘要 |
| `content_source_url` | 否 | 原文或来源地址 |
| `need_open_comment` | 否 | `0` 关闭、`1` 开启评论 |
| `only_fans_can_comment` | 否 | `0` 所有人、`1` 仅关注后评论 |

### 第四步：创建草稿

```powershell
python scripts/wechat_draft.py create-draft .\article.json
```

这个命令不会发送文章，也不会自动发布。它只会创建一份草稿，供你在公众号后台继续审核。

## 在 Codex 中怎么说

安装并重启 Codex 后，可以直接提出类似需求：

```text
检查我的微信公众号草稿箱凭据是否可用。
```

```text
把 D:\公众号\2026-07-10\article.html 创建为公众号草稿；先确认标题和目标账号，不要发布。
```

Codex 应先检查凭据、确认目标账户和文章标题，再上传封面、创建草稿。不要要求它跳过人工确认或自动发布。

## 常见问题

### `doctor` 显示缺少凭据

重新打开终端再运行 `doctor`。如果仍失败，检查环境变量名称是否严格为 `WECHAT_APPID` 和 `WECHAT_SECRET`，以及是否设置在当前 Windows 用户下。

### 接口提示 IP 不在白名单

这通常不是脚本故障。请到公众号后台开发者设置中更新 API 白名单，确认填写的是当前网络实际对外的公网 IP，然后重试。

### 草稿创建成功，但正文排版不理想

先在公众号编辑器中预览 HTML，再调整文章 HTML 后重新创建草稿。此 Skill 负责提交草稿，不替代排版与内容审核。

### 可以自动群发吗

不可以，也不会加入该能力。本项目刻意限定为草稿创建工具，避免绕过最后的人工检查。

## 安全设计

- 不调用群发、发布或删除接口；
- AppSecret 只从本机环境变量读取；
- 不需要安装第三方 Python 包；
- 命令行结果采用 JSON，便于接入自动化流程；
- 草稿完成后，仍由你在公众号后台进行最终审核与发布。

## 参与贡献

欢迎提交改进。提交前请不要上传 AppID、AppSecret、访问令牌、真实文章内容或无授权图片，并保持“只创建草稿”的安全边界。具体要求见 [CONTRIBUTING.md](CONTRIBUTING.md)，安全问题请参阅 [SECURITY.md](SECURITY.md)。

## 本地验证

```powershell
python scripts/wechat_draft.py doctor
python C:\Users\侯晓宇\.codex\skills\.system\skill-creator\scripts\quick_validate.py .
```

## 许可证

本项目采用 [MIT License](LICENSE)。
