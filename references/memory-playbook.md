# 长期记忆规则

## 目标

长期监控的价值来自历史上下文，而不是单次抓数。每个任务必须把历史日报、周报、结构化快照、关键判断和待验证假设沉淀到 `memory/{task_id}/`。

`rolling-memory.md` 面向人阅读，必须用中文写稳定模式、关键拐点、当前判断和待验证问题。`signal-ledger.jsonl` 和 `hypotheses.yaml` 是机器可读文件，字段名和状态枚举可以保留英文，但 `summary`、`evidence`、`statement` 应尽量使用中文。

## 记忆文件

| 文件 | 用途 |
| --- | --- |
| `rolling-memory.md` | 人工可读的长期记忆摘要，记录稳定模式、关键拐点和长期结论 |
| `signal-ledger.jsonl` | 机器可读的信号流水，每行一个 JSON 对象 |
| `hypotheses.yaml` | 待验证假设、状态、证据计数和复盘记录 |

## 读取顺序

每次运行先读取：

1. `tasks/{task_id}.yaml`
2. `memory/{task_id}/rolling-memory.md`
3. `memory/{task_id}/hypotheses.yaml`
4. `memory/{task_id}/signal-ledger.jsonl` 的最近记录
5. 最近 `memory.recent_daily_reports` 篇日报
6. 最近 `memory.recent_weekly_reports` 篇周报
7. 最近结构化快照

不要每次全文读取所有历史报告。更早历史只通过 `rolling-memory.md` 和 `signal-ledger.jsonl` 进入分析。

## 信号流水格式

`signal-ledger.jsonl` 每行使用下面字段：

```json
{"date":"2026-04-20","cadence":"daily","signal_key":"price-drop-hero-asin","dimension":"price","status":"new","summary":"Hero ASIN 价格跌破历史低位","evidence":"当前价格低于上次快照","confidence":"medium"}
```

字段规则：

| 字段 | 规则 |
| --- | --- |
| `date` | 运行日期，建议 ISO 日期 |
| `cadence` | `daily` 或 `weekly` |
| `signal_key` | 稳定短横线 ID，同类信号必须复用同一个 key |
| `dimension` | `price`、`traffic`、`review`、`supply-chain`、`capital` 等 |
| `status` | 只允许 `new`、`watching`、`confirmed`、`reversed`、`archived` |
| `summary` | 一句话中文说明信号 |
| `evidence` | 中文说明证据口径 |
| `confidence` | `high`、`medium`、`low` |

## 信号生命周期

- `new`
  - 首次出现的新信号
- `watching`
  - 多次出现但证据不足，尚未达到确认阈值
- `confirmed`
  - 同类证据累计达到 `memory.signal_confirmation_threshold`
- `reversed`
  - 新证据与历史判断相反
- `archived`
  - 不再影响当前策略，但保留历史

旧结论被推翻时标记 `reversed`，不要删除。

## 日报规则

日报只做轻量 memory 更新：

- 判断本次变化是噪音、延续、异常、趋势反转，还是新信号
- 只有满足任一条件才进入 memory：
  - 影响价格、流量、Review、上新、断货、库存或雷达评分
  - 连续出现并可能形成趋势
  - 与历史判断相反
  - 需要周报复盘
- 普通日内小波动不进入 memory，只在日报正文说明

## 周报规则

周报必须复盘 memory：

- 更新 `rolling-memory.md` 的稳定模式和关键拐点
- 复盘 `hypotheses.yaml` 中所有 `new`、`watching`、`confirmed`、`reversed` 状态假设
- 将达到确认阈值的信号升级为 `confirmed`
- 将被相反证据推翻的判断标为 `reversed`
- 将不再影响当前策略的历史信号标为 `archived`

## 假设处理

假设用于表达尚未完全确认的战略判断，例如：

- 该竞品是流量型选手
- 低价可能是清库存而非价格战
- 该品牌具备供应链复用优势

每个假设至少包含：

- `id`
- `statement`
- `status`
- `evidence_count`
- `contradiction_count`
- `confidence`
- `last_reviewed`
- `next_review`

状态只允许：

- `new`
- `watching`
- `confirmed`
- `reversed`
- `archived`

## 噪音控制

不要把所有变化都写入 memory。优先保留：

- 反复出现的变化
- 与资金效率、供应链效率、转化效率、流量效率相关的变化
- 会影响下周策略的变化
- 反转历史判断的变化

无法判断的信号保留为 `watching`，并明确需要哪些后续证据。
