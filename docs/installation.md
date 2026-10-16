# 安装与配置

## 一句话安装

推荐直接把下面这句话发给 Codex，让它帮你安装：

```text
请帮我安装这个 codex-ppt skill，链接是：https://github.com/shx99717/codex-ppt-skill
```

## Codex 手动安装

在命令行中执行以下命令，将 `codex-ppt` skill 安装到 Codex 全局 skills 目录：

```bash
npx -y skills@latest add shx99717/codex-ppt-skill \
  --skill codex-ppt \
  --agent codex \
  --global
```

安装后重启 Codex，让新 skill 生效。

也可以从 [GitHub Releases](https://github.com/shx99717/codex-ppt-skill/releases) 下载 `codex-ppt-skill-v*.zip`，解压后把其中的 `codex-ppt` 文件夹放到 `~/.codex/skills/codex-ppt`，然后重启 Codex。

如果你在本地开发这个仓库，可以把 skill 目录软链接到 Codex skills 目录，方便实时调试修改：

```bash
mkdir -p ~/.codex/skills
ln -s /path/to/codex-ppt-skill/skills/codex-ppt ~/.codex/skills/codex-ppt
```

## OpenClaw 安装

```bash
openclaw skills install codex-ppt
```

如果使用 OpenClaw 的 skill allowlist，需要把 `codex-ppt` 加入允许列表。

## Claude Code / Hermes Agent

Claude Code：

```bash
npx -y skills@latest add shx99717/codex-ppt-skill \
  --skill codex-ppt \
  --agent claude-code \
  --global
```

Hermes Agent：

```bash
npx -y skills@latest add shx99717/codex-ppt-skill \
  --skill codex-ppt \
  --agent hermes-agent \
  --global
```

常见目标目录：Claude Code 使用 `~/.claude/skills/codex-ppt`，Hermes Agent 使用 `~/.hermes/skills/codex-ppt`。本地开发时同样可以用软链接替代复制。

## 更新 skill

推荐直接把下面这句话发给你的 agent，让它帮你更新：

```text
请帮我更新 codex-ppt skill 到最新版本，仓库是：https://github.com/shx99717/codex-ppt-skill
```

手动更新时，重新执行上面对应 agent 的安装命令即可，会用最新版本覆盖已安装的 skill；也可以从 [GitHub Releases](https://github.com/shx99717/codex-ppt-skill/releases) 下载最新的 `codex-ppt-skill-v*.zip`，解压后替换原来的 `codex-ppt` 目录。更新完成后重启 agent 生效。

更新是安全的：API key 等运行时配置保存在 `~/.codex-ppt-skill/.env`，个人风格库保存在 `~/.codex-ppt-skill/references/`，都在 skill 安装目录之外，更新或重装不会丢失。每个版本的变更内容可以查看 [Releases 页面](https://github.com/shx99717/codex-ppt-skill/releases)或仓库的 `CHANGELOG.md`。

## 生图模型配置

优先使用当前可调用的 Codex `image_gen` 或 Cursor `GenerateImage`，以实时工具 schema 为准；原生工具的模型由宿主管理。Codex 可通过提示词请求 16:9 或 4:3，无需 size 参数；Cursor 应传入受支持的 `aspect_ratio`。测量实际文件宽高并检查 2% 比例容差，不能把分辨率请求当作原生 4K 的证明。API 回退复用明确配置的供应商模型；未配置时根据当前官方文档选择，不设固定模型默认值。通过真实输入机制附加全部源图和风格图，并记录绑定当前尝试的提交证据。原生和桥接证据保留为代理报告；CLI 验证依赖已登记的成功执行。历史文件可查看，但新的托管执行和组装需要重新编译及新的证据。仅支持 16:9 和 4:3，不自动转换旧比例。

## 如何确认生图模型可用？


- 如果你使用第三方中转 API 接入 Codex，可以让它生成一张包含复杂中文文本的图片，例如要求用行楷写一首诗。观察是否能正常生图，以及生成的图里是否有中文字体错误。如果一切正常，也无需配置。
如果原生工具和已安装的桥接路径均不可用，可明确选择 API 供应商并配置其文档支持的模型。订阅本身不能保证当前会话存在可调用的原生工具。

通常不需要手动配置生图模型。你在使用 Codex PPT 的过程中，AI 会自动检测生图后端；如果不可用，会提示你配置生图后端 API，并引导你完成配置。

## 第三方 API 注意事项

本 skill 内置了一个适配 OpenAI 官方生图方式的脚本。如果你用的是第三方生图中转 API，可以尝试提供：

- 中转站的 base URL
  - 中转站示例如果是 `https://xxx/v1/images/generations`，base URL 填 `https://xxx/v1`。
  - 如果中转站已经给的是 `https://xxx/v1`，不要再加一层，避免 `.../v1/v1`。
  - 如果是官方 OpenAI，`OPENAI_BASE_URL` 可以不填，默认就是官方 `https://api.openai.com/v1`。
- 中转站的 API key
- 中转站文档中的准确模型 ID

将上述信息提供给 AI 之后，尝试让其生图。如果跑不通，则可能你使用的中转站有自定义的生图使用方案，不完全兼容 OpenAI 生图接口。请将中转站官方的生图使用文档发给 AI，让它学习并适配生图脚本。
