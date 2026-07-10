# Security Policy

## Reporting a vulnerability

请不要在公开 Issue 中提交可能泄露 AppSecret、访问令牌或公众号权限的问题。请通过 GitHub 账户 `hxy180` 的个人主页联系维护者，并提供最小可复现信息。

## Credential handling

- 仅使用本机环境变量 `WECHAT_APPID` 与 `WECHAT_SECRET`；
- 不要提交 `.env`、文章 JSON、图片或终端输出中的敏感字段；
- 如怀疑 AppSecret 泄露，请立即在微信公众号后台重置，并更新本机环境变量。
