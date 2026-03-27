# Reporting Playbook

## Core Rule

监控报告不是一次性总结，而是持续追加的运行日志。每次运行都应在原文档中追加一个新的日期分节，而不是覆盖旧内容。

## Daily Report

日报优先回答三个问题：

1. 今天看到了什么变化
2. 哪些变化值得立刻处理
3. 哪些点还需要继续观察

建议结构：

1. `Executive Summary`
2. `KPI Snapshot`
3. `Key Changes`
4. `Risks and Actions`
5. `Next Watch`

建议表格：

| Block | Required |
| --- | --- |
| `KPI Snapshot` | Yes |
| `Key Changes` | Yes |
| `Risk / Action` | Yes |

## Weekly Report

周报优先回答四个问题：

1. 这一周的主线变化是什么
2. 谁是赢家，谁是输家
3. 是战术波动还是结构变化
4. 下周应该怎么调动作

建议结构：

1. `Week Summary`
2. `Scoreboard`
3. `Structural Changes`
4. `Review / Keyword / Traffic Themes`
5. `Actions for Next Week`

建议表格：

| Block | Required |
| --- | --- |
| `Scoreboard` | Yes |
| `Structural Changes` | Yes |
| `Action List` | Yes |

## Comparison Logic

日报基线：

- 优先对比上一次同任务快照
- 没有快照时，对比上一次日报
- 还没有日报时，写成“首次建档”

周报基线：

- 优先对比上一次周报
- 没有周报时，对比最近 7 天的首个可用快照
- 仍然没有历史时，写成“本周为第一周观察窗口”

所有比较都要写具体日期，不要只写“较上周”或“较昨日”。

## Monitor-Type Emphasis

### `asin`

日报重点：

- 价格和 Coupon 变化
- 销量、排名或趋势拐点
- 新评论里的高频信号

周报重点：

- 流量结构变化
- 评论主题累计变化
- 价格策略是否持续

### `multi-asin`

日报重点：

- 谁涨、谁跌、谁促销
- 头部 3 个差异点

周报重点：

- 竞品位次变化
- 价格带和评分带的重新分布
- 关键词或流量重心的迁移

### `seller`

日报重点：

- 上新、下架、异常调价
- 头部 SKU 的即时变化

周报重点：

- 商品池扩缩张
- 卖家主推方向是否切换
- 是否出现新的核心 SKU

### `brand`

日报重点：

- 新品、促销、头部款波动
- 品牌价格带或评论波动

周报重点：

- 品牌组合变化
- 头部集中度
- 新品节奏和品牌覆盖变化

## Language and Evidence Rules

- 中文为主，保留 ASIN、品牌名、卖家名、关键词原文
- 每个关键判断至少有一个证据落点
- 如果某项数据是“本月口径”或“滚动窗口”，要明确标注
- 不足以确认时，直接写“不足以确认”

## Action Style

动作建议必须具体到能执行：

- 价格动作
- 广告或关键词动作
- 内容或评论应对动作
- 新品跟进动作
- 继续观察动作

避免写成纯抽象建议，例如“继续优化运营”。
