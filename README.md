# amazon-competitor-monitor

## 🚀 Way to AIC | 通往 AI 电商之路
---
### 🌐 官网 Website
- https://waytoaic.com  
- https://www.waytoaic.com  
---

### 👥 社群招募 Community
`Way to AIC 社群招募 | WaytoAIC.com`

<p align="center">
  <img src="https://github.com/user-attachments/assets/d9f8bbf4-2056-4780-975d-86c885b52bab" width="70%">
</p>

---

### 📣 公众号 WeChat Official Account
`维正 WaytoAIC`

<p align="center">
  <img src="https://github.com/user-attachments/assets/71c71a5c-e68a-4f30-9afb-f2b056619991" width="300">
</p>

---

### 🧠 知识星球 Xiaozhixing
`AI电商之路 WaytoAIC`

<p align="center">
  <img src="https://github.com/user-attachments/assets/9eccef07-0e84-45a7-a415-affcb18c928d" width="200">
  <img src="https://github.com/user-attachments/assets/4e99fbc3-1981-4fee-b113-c9821141102d" width="400">
</p>

---

### 🧩 About Way to AIC

**AIC = AI Commerce**

在 AI 重塑商业的时代，我们希望和每一个拥抱 AI 的卖家：

- 找到场景  
- 定义问题  
- 积累能力  
- 设计系统  

共同通往 AI 电商之路。

> Way to AIC 不是教学，不是工具，  
> 而是一条所有电商人共同走的进化之路。

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
## Quick Install

```bash
# Codex
curl -fsSL https://raw.githubusercontent.com/WaytoAIC/amazon-competitor-monitor/v1.1.1/install.sh | bash -s -- --target codex --ref v1.1.1
```

```bash
# OpenClaw
curl -fsSL https://raw.githubusercontent.com/WaytoAIC/amazon-competitor-monitor/v1.1.1/install.sh | bash -s -- --target openclaw --ref v1.1.1
```

```bash
# Install into a custom skills directory
curl -fsSL https://raw.githubusercontent.com/WaytoAIC/amazon-competitor-monitor/v1.1.1/install.sh | bash -s -- --dest "$(pwd)/skills" --ref v1.1.1
```

安装后重启 Codex / OpenClaw。

---

一个面向 Amazon 竞品监控的 Codex skill，支持按单个 ASIN、多 ASIN、特定卖家或特定品牌建立独立监控任务，并分别维护日报、周报、快照和长期记忆。

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
- 为每个任务分别维护独立的日报、周报、快照和 memory
- 将历史日报、周报、快照和关键判断沉淀成长期任务记忆
- 支持盈利模型雷达：流量效率、转化效率、供应链效率、资金实力
- 支持信号生命周期：`new`、`watching`、`confirmed`、`reversed`、`archived`
- 支持将日报 / 周报压缩成展示卡，输出同款风格的 HTML + PNG
- 报告正文默认中文输出，ASIN、品牌名、卖家名、关键词等专有名词保留原文
- 提供工作区初始化脚本，快速生成 `tasks/`、`docs/`、`snapshots/`、`memory/`、`logs/`

### 监控规则

- 每个任务只允许一个监控对象类型
- 每个任务只允许一个 MCP
- 默认 MCP 是 `sellersprite-mcp`
- 可选 MCP 是 `sorftime_mcp`
- 多任务并行时，必须分别写入各自文档，不合并在同一份日报或周报中
- 后续分析必须先读取该任务历史记忆，再判断本次变化是噪音、延续、异常、趋势反转还是新信号
- 供应链效率和资金实力默认使用代理指标判断，必须标注置信度
- 日报、周报和长期记忆的标题、表头、结论、动作建议都使用中文

### 仓库结构

- 主 skill 入口：[SKILL.md](./SKILL.md)
- UI 元数据：[agents/openai.yaml](./agents/openai.yaml)
- 完整中文说明与使用 SOP：[docs/usage-sop.zh.md](./docs/usage-sop.zh.md)
- 任务 schema：[references/task-schema.md](./references/task-schema.md)
- MCP 选型规则：[references/tool-mapping.md](./references/tool-mapping.md)
- 报告写法规则：[references/reporting-playbook.md](./references/reporting-playbook.md)
- 展示卡规则：[references/card-playbook.md](./references/card-playbook.md)
- 长期记忆规则：[references/memory-playbook.md](./references/memory-playbook.md)
- 盈利模型雷达：[references/profit-model-playbook.md](./references/profit-model-playbook.md)
- 工作区初始化脚本：[scripts/init_monitor_workspace.py](./scripts/init_monitor_workspace.py)
- 信号记忆更新脚本：[scripts/update_memory.py](./scripts/update_memory.py)
- 日报 / 周报展示卡脚本：[scripts/generate_report_card.py](./scripts/generate_report_card.py)
- 任务与报告模板：
  - [assets/task-config.template.yaml](./assets/task-config.template.yaml)
  - [assets/daily-report.template.md](./assets/daily-report.template.md)
  - [assets/weekly-report.template.md](./assets/weekly-report.template.md)

### 推荐使用方式

直接在 Codex 里说：

- `用 $amazon-competitor-monitor 帮我建一个品牌监控任务，监控美国站 Anker，输出日报和周报`
- `用 $amazon-competitor-monitor 帮我建一个多 ASIN 监控任务，只用 sellersprite-mcp`
- `用 $amazon-competitor-monitor 更新这个卖家监控周报`
- `用 $amazon-competitor-monitor 基于历史周报更新竞品盈利模型雷达`
- `用 $amazon-competitor-monitor 把这个 ASIN 日报和周报分别生成 HTML+PNG 展示卡`

### 初始化工作区示例

```bash
python3 scripts/init_monitor_workspace.py \
  --workspace "$(pwd)" \
  --task-id brand-anker-us \
  --monitor-type brand \
  --target Anker \
  --mcp sellersprite-mcp \
  --marketplace US \
  --radar
```

### 记录长期信号示例

```bash
python3 scripts/update_memory.py \
  --workspace "$(pwd)" \
  --task-id brand-anker-us \
  --signal-key price-drop-hero-asin \
  --dimension price \
  --summary "Hero ASIN price dropped below its recent floor" \
  --evidence "Observed in daily monitor versus previous snapshot" \
  --confidence medium
```

### 生成展示卡示例

```bash
python3 scripts/generate_report_card.py \
  --workspace "$(pwd)" \
  --task-id brand-anker-us \
  --cadence daily \
  --date 2026-04-21 \
  --screenshot
```

```bash
python3 scripts/generate_report_card.py \
  --workspace "$(pwd)" \
  --task-id brand-anker-us \
  --cadence weekly \
  --screenshot
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

Each task keeps its own daily report, weekly report, snapshot history, and long-term memory, and each task must use exactly one MCP source.

### What this skill helps with

- scaffolding a clean workspace for Amazon competitor monitoring
- creating per-task YAML configs and report docs
- enforcing one-task-one-MCP rules
- choosing between `sellersprite-mcp` and `sorftime_mcp`
- preserving task memory across daily and weekly reports
- scoring profit-model radar dimensions with evidence and confidence
- rendering compact daily and weekly presentation cards as HTML + PNG
- generating Chinese monitoring reports backed by a clear evidence structure while preserving ASINs, brand names, seller names, and keywords in their original form

### Included files

- Main skill: [SKILL.md](./SKILL.md)
- UI metadata: [agents/openai.yaml](./agents/openai.yaml)
- Task schema: [references/task-schema.md](./references/task-schema.md)
- Tool mapping: [references/tool-mapping.md](./references/tool-mapping.md)
- Reporting guide: [references/reporting-playbook.md](./references/reporting-playbook.md)
- Report card guide: [references/card-playbook.md](./references/card-playbook.md)
- Memory guide: [references/memory-playbook.md](./references/memory-playbook.md)
- Profit model guide: [references/profit-model-playbook.md](./references/profit-model-playbook.md)
- Workspace bootstrap script: [scripts/init_monitor_workspace.py](./scripts/init_monitor_workspace.py)
- Memory update script: [scripts/update_memory.py](./scripts/update_memory.py)
- HTML + PNG card script: [scripts/generate_report_card.py](./scripts/generate_report_card.py)

### One-command workspace bootstrap

```bash
python3 scripts/init_monitor_workspace.py \
  --workspace "$(pwd)" \
  --task-id brand-anker-us \
  --monitor-type brand \
  --target Anker \
  --mcp sellersprite-mcp \
  --marketplace US \
  --radar
```

### License note

This repository is public and source-available, but commercial use is restricted. See [LICENSE.md](./LICENSE.md) and [ADDITIONAL_TERMS.md](./ADDITIONAL_TERMS.md).
