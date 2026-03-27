# amazon-competitor-monitor

## Way to AIC | 通往AI电商之路

Fixed README prefix for Way to AIC repositories.

- 官网 / Website: [waytoaic.com](https://waytoaic.com) | [www.waytoaic.com](https://www.waytoaic.com)
- 社群招募 / Community: `Way to AIC社群招募 | WaytoAIC.com`
- 公众号 / WeChat Official Account: `维正 WaytoAIC`
- 知识星球 / Xiaozhixing: `AI电商之路 WaytoAIC`
- AIC = `AI Commerce`

在 AI 重塑商业的时代，我们希望和每一个拥抱 AI 的卖家，找到场景，定义问题，积累能力，设计系统，共同通往 AI 电商之路。

Way to AIC 不是教学，不是工具，而是一条所有电商人共同走的进化之路。

后续 Way to AIC 相关 GitHub 项目，默认都应在 README 顶部保留这一前缀区块。

### WaytoAIC 理念 | Principles

| 中文 | English |
|---|---|
| 场景先于方法 | Context before method |
| AI 的价值来自真实业务场景，而不是技术本身。 | AI creates value through real business contexts, not through technology alone. |
| 问题先于答案 | Problem before answer |
| 定义问题，比拥有工具更重要。 | Defining the problem matters more than collecting tools. |
| 系统胜过技巧 | System over tricks |
| 技巧是术，系统才是道，决定卖家的上限。 | Tricks are tactical; systems define long-term leverage and ceiling. |
| 共创优于独行 | Co-creation over solo progress |
| 我们相信，真正的进化发生在共同探索的过程中。 | Real evolution happens through shared exploration. |

---

中文 | [English](#english)

## Quick Install

```bash
# Codex
curl -fsSL https://raw.githubusercontent.com/WaytoAIC/amazon-competitor-monitor/v1.0.0/install.sh | bash -s -- --target codex --ref v1.0.0
```

```bash
# OpenClaw
curl -fsSL https://raw.githubusercontent.com/WaytoAIC/amazon-competitor-monitor/v1.0.0/install.sh | bash -s -- --target openclaw --ref v1.0.0
```

```bash
# Install into a custom skills directory
curl -fsSL https://raw.githubusercontent.com/WaytoAIC/amazon-competitor-monitor/v1.0.0/install.sh | bash -s -- --dest "$(pwd)/skills" --ref v1.0.0
```

安装后重启 Codex / OpenClaw。

---

一个面向 Amazon 竞品监控的 Codex skill，支持按单个 ASIN、多 ASIN、特定卖家或特定品牌建立独立监控任务，并分别维护日报和周报文档。

## 中文

### 这个 skill 会帮你做什么

- 为 Amazon 竞品监控建立统一的任务配置结构
- 支持 4 类监控对象：
  - 单个 ASIN
  - 多 ASIN
  - 特定卖家
  - 特定品牌
- 支持 `daily` / `weekly` 两种输出节奏
- 强制一任务一 MCP，不混用数据源
- 为每个任务分别维护独立的日报、周报和快照目录
- 提供工作区初始化脚本，快速生成 `tasks/`、`docs/`、`snapshots/`、`logs/`

### 监控规则

- 每个任务只允许一个监控对象类型
- 每个任务只允许一个 MCP
- 默认 MCP 是 `sellersprite-mcp`
- 可选 MCP 是 `sorftime_mcp`
- 多任务并行时，必须分别写入各自文档，不合并在同一份日报或周报中

### 仓库结构

- 主 skill 入口：[SKILL.md](./SKILL.md)
- UI 元数据：[agents/openai.yaml](./agents/openai.yaml)
- 任务 schema：[references/task-schema.md](./references/task-schema.md)
- MCP 选型规则：[references/tool-mapping.md](./references/tool-mapping.md)
- 报告写法规则：[references/reporting-playbook.md](./references/reporting-playbook.md)
- 工作区初始化脚本：[scripts/init_monitor_workspace.py](./scripts/init_monitor_workspace.py)
- 任务与报告模板：
  - [assets/task-config.template.yaml](./assets/task-config.template.yaml)
  - [assets/daily-report.template.md](./assets/daily-report.template.md)
  - [assets/weekly-report.template.md](./assets/weekly-report.template.md)

### 推荐使用方式

直接在 Codex 里说：

- `用 $amazon-competitor-monitor 帮我建一个品牌监控任务，监控美国站 Anker，输出日报和周报`
- `用 $amazon-competitor-monitor 帮我建一个多 ASIN 监控任务，只用 sellersprite-mcp`
- `用 $amazon-competitor-monitor 更新这个卖家监控周报`

### 初始化工作区示例

```bash
python3 scripts/init_monitor_workspace.py \
  --workspace "$(pwd)" \
  --task-id brand-anker-us \
  --monitor-type brand \
  --target Anker \
  --mcp sellersprite-mcp \
  --marketplace US
```

### 许可说明

- 当前仓库是公开可见、可学习和可使用的 `source-available` 仓库
- 默认不允许商用
- 如果你基于本仓库做修改、二次分发或组合进更大的功能并对外发布，需要公开对应源码

---

## English

This repository provides a Codex skill for structured Amazon competitor monitoring.

It supports building independent monitoring tasks for:

- a single ASIN
- multiple ASINs
- a specific seller
- a specific brand

Each task keeps its own daily report, weekly report, and snapshot history, and each task must use exactly one MCP source.

### What this skill helps with

- scaffolding a clean workspace for Amazon competitor monitoring
- creating per-task YAML configs and report docs
- enforcing one-task-one-MCP rules
- choosing between `sellersprite-mcp` and `sorftime_mcp`
- generating Chinese-first monitoring reports backed by a clear evidence structure

### Included files

- Main skill: [SKILL.md](./SKILL.md)
- UI metadata: [agents/openai.yaml](./agents/openai.yaml)
- Task schema: [references/task-schema.md](./references/task-schema.md)
- Tool mapping: [references/tool-mapping.md](./references/tool-mapping.md)
- Reporting guide: [references/reporting-playbook.md](./references/reporting-playbook.md)
- Workspace bootstrap script: [scripts/init_monitor_workspace.py](./scripts/init_monitor_workspace.py)

### One-command workspace bootstrap

```bash
python3 scripts/init_monitor_workspace.py \
  --workspace "$(pwd)" \
  --task-id brand-anker-us \
  --monitor-type brand \
  --target Anker \
  --mcp sellersprite-mcp \
  --marketplace US
```

### License note

This repository is public and source-available, but commercial use is restricted. See [LICENSE.md](./LICENSE.md) and [ADDITIONAL_TERMS.md](./ADDITIONAL_TERMS.md).
