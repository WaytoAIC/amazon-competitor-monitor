# Task Schema

## Workspace Layout

推荐每个监控工作区使用下面的固定目录结构：

```text
workspace/
├── tasks/
├── docs/
├── snapshots/
├── memory/
└── logs/
```

- `tasks/`
  - 一任务一配置文件，文件名建议与 `task_id` 一致
- `docs/`
  - 每个任务独立维护日报和周报文档
- `snapshots/`
  - 保存结构化快照，便于做跨日或跨周对比
- `memory/`
  - 一任务一目录，沉淀长期模式、信号流水和待验证假设
- `logs/`
  - 保存运行日志、失败记录或辅助说明

## Required Fields

| Field | Type | Rule |
| --- | --- | --- |
| `task_id` | string | 小写短横线命名，跨文档和快照保持一致 |
| `enabled` | boolean | 关闭的任务不要执行 |
| `priority` | integer | 多任务时按从高到低执行 |
| `marketplace` | string | Amazon 站点，例如 `US`、`JP`、`DE` |
| `monitor_type` | string | 仅允许 `asin`、`multi-asin`、`seller`、`brand` |
| `targets` | object | 目标字段必须与 `monitor_type` 一一对应 |
| `mcp` | string | 仅允许 `sellersprite-mcp` 或 `sorftime_mcp` |
| `cadences` | list | 至少一个值，允许 `daily`、`weekly` |
| `outputs` | object | 至少包含 `daily_doc`、`weekly_doc`、`snapshot_dir` |
| `focus` | list | 说明本任务要优先关注哪些维度 |
| `analysis_layers` | list | 默认 `monitoring`，可选 `profit-model`、`strategy-radar` |
| `memory` | object | 长期监控记忆配置，缺失时按默认值补齐 |

## Target Rules By Monitor Type

| `monitor_type` | `targets` shape | Rule |
| --- | --- | --- |
| `asin` | `asin: "B0..."` | 只能有一个 ASIN |
| `multi-asin` | `asins: ["B0...", "B0..."]` | 至少两个 ASIN，建议不超过 20 个 |
| `seller` | `seller: "SellerName"` | 只填一个卖家识别名 |
| `brand` | `brand: "BrandName"` | 只填一个品牌 |

如果同一主体既要做品牌监控又要做卖家监控，不要共用一个任务，应拆成两个任务。

## Suggested Focus Values

可选 `focus` 值建议统一使用以下词汇：

- `price`
- `coupon`
- `sales`
- `bsr`
- `rating`
- `review`
- `traffic`
- `keyword`
- `catalog`
- `new-listing`
- `seller-pool`
- `brand-concentration`
- `profit-model`
- `strategy-radar`

## Analysis Layers

`analysis_layers` 只允许以下值：

- `monitoring`
- `profit-model`
- `strategy-radar`

默认值：

```yaml
analysis_layers:
  - "monitoring"
```

启用盈利模型雷达时：

```yaml
analysis_layers:
  - "monitoring"
  - "profit-model"
  - "strategy-radar"
```

## Memory Defaults

缺少 `memory` 字段时，按下面默认值执行：

```yaml
memory:
  enabled: true
  recent_daily_reports: 7
  recent_weekly_reports: 4
  signal_confirmation_threshold: 3
  hypothesis_review_cadence: "weekly"
  rolling_memory_doc: "memory/{task_id}/rolling-memory.md"
  signal_ledger: "memory/{task_id}/signal-ledger.jsonl"
  hypotheses_doc: "memory/{task_id}/hypotheses.yaml"
```

字段含义：

| Field | Rule |
| --- | --- |
| `enabled` | 默认开启；只有显式 `false` 才跳过 memory |
| `recent_daily_reports` | 日报分析时读取的最近日报数量 |
| `recent_weekly_reports` | 周报分析时读取的最近周报数量 |
| `signal_confirmation_threshold` | 同类信号累计达到该次数后可从 `watching` 升级为 `confirmed` |
| `hypothesis_review_cadence` | 默认每周复盘假设 |
| `rolling_memory_doc` | 人工可读长期记忆 |
| `signal_ledger` | JSONL 信号流水 |
| `hypotheses_doc` | 待验证假设 |

## Canonical Example

```yaml
task_id: "brand-anker-us"
enabled: true
priority: 80
marketplace: "US"
monitor_type: "brand"
targets:
  brand: "Anker"
mcp: "sellersprite-mcp"
cadences:
  - "daily"
  - "weekly"
comparison:
  daily_lookback_days: 1
  weekly_lookback_days: 7
outputs:
  daily_doc: "docs/brand-anker-us-daily.md"
  weekly_doc: "docs/brand-anker-us-weekly.md"
  snapshot_dir: "snapshots/brand-anker-us"
memory:
  enabled: true
  recent_daily_reports: 7
  recent_weekly_reports: 4
  signal_confirmation_threshold: 3
  hypothesis_review_cadence: "weekly"
  rolling_memory_doc: "memory/brand-anker-us/rolling-memory.md"
  signal_ledger: "memory/brand-anker-us/signal-ledger.jsonl"
  hypotheses_doc: "memory/brand-anker-us/hypotheses.yaml"
analysis_layers:
  - "monitoring"
focus:
  - "price"
  - "coupon"
  - "sales"
  - "review"
  - "keyword"
  - "catalog"
notes: "Track hero ASIN movement, promotions, and new launches."
```

## Field Handling Rules

- 一个 YAML 文件只放一个任务，不要做任务数组。
- `daily_doc` 和 `weekly_doc` 建议始终保留，即使当前只启用其中一个 cadence。
- `memory/{task_id}/` 必须与任务一一对应，不要跨任务复用。
- 旧任务缺少 `memory` 或 `analysis_layers` 时视为合法，执行时按默认值补齐。
- `snapshot_dir` 里的快照应按运行日期命名，例如：
  - `2026-03-27.daily.json`
  - `2026-W13.weekly.json`
- 当任务首次建档时，可以先没有快照；从第二次运行开始，应尽量保留结构化对比依据。
- 如果任务切换 MCP，应视为重大口径变化，在文档中明确标注，并尽量新开一个任务而不是覆盖旧任务。
