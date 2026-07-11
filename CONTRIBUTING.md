# Contributing

感谢贡献。请保持本项目的核心边界：只支持创建草稿，绝不加入群发、发布或删除公众号内容的功能。

## 提交前检查

1. 不要提交任何 AppID、AppSecret、访问令牌、封面素材或真实文章数据；
2. 保持 Python 标准库实现，除非新增依赖有明确必要；
3. 运行以下检查：

```powershell
python scripts/wechat_draft.py doctor
# 仅在维护 Codex Skill 时运行；替换为你自己的 Codex 安装目录
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .
```

4. 在 Pull Request 中说明变更内容、验证方式及其是否影响 API 请求。

## 代码约定

- 命令行输出使用 JSON，便于自动化解析；
- 错误不得输出密钥、访问令牌或完整请求 URL；
- 新增接口前，先确认它不会绕过人工审核或触及发布操作。
