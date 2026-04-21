# Amazon 竞品监控 Skill 说明与使用 SOP

适用项目：[WaytoAIC/amazon-competitor-monitor](https://github.com/WaytoAIC/amazon-competitor-monitor)
适用版本：`v1.1.1`
本 SOP 适合给运营、广告、选品和 Listing 团队使用，用来建立和维护 Amazon 竞品长期监控任务。

---

## 1. 这个 Skill 是什么

`amazon-competitor-monitor` 是一个给 Codex / OpenClaw 使用的 Amazon 竞品监控技能包。它不是一个单独自动抓数的软件，而是一套标准工作流：

- 用统一 YAML 配置定义每个监控任务。
- 通过 Codex 调用指定 MCP 数据源抓取竞品数据。
- 为每个任务分别维护日报、周报、快照和长期记忆。
- 强制“一任务一监控对象、一任务一 MCP”，避免不同数据源口径混在一起。
- 把竞品变化沉淀成长期信号、假设和策略判断。
- 支持盈利模型雷达，从流量效率、转化效率、供应链效率、资金实力四个维度拆解对手。

一句话理解：它把“今天看一下竞品”升级成“同一套口径持续跟踪竞品，并能复盘历史变化”。

---

## 2. 它能解决什么问题

| 场景 | 能做什么 | 输出物 |
| --- | --- | --- |
| 盯单个 ASIN | 监控价格、Coupon、排名、评论、流量词、广告/自然结构 | 单 ASIN 日报、周报、快照、长期记忆 |
| 盯多个 ASIN | 对比一组竞品谁涨、谁跌、谁更值得打 | 多 ASIN 对比日报、周报 |
| 盯卖家 | 监控某个卖家商品池、上新、下架、头部 SKU、价格带 | 卖家监控报告 |
| 盯品牌 | 监控品牌商品池、头部款、新品节奏、品牌集中度 | 品牌监控报告 |
| 做竞品策略 | 判断对手是流量型、品牌型、工厂型、资金型还是均衡型 | 盈利模型雷达、策略地图 |
| 做长期复盘 | 判断变化是噪音、延续、异常、趋势反转还是新信号 | `rolling-memory.md`、`signal-ledger.jsonl`、`hypotheses.yaml` |

---

## 3. 它不能替代什么

| 不适合直接替代的工作 | 原因 | 正确做法 |
| --- | --- | --- |
| 精确利润核算 | 公开数据无法知道对手真实成本、库存、广告花费 | 用代理指标判断，并标注置信度 |
| 完全无人值守的抓数系统 | Skill 负责工作流，真正抓数依赖 Codex 和 MCP | 如果要自动化，需要另行配置定时任务或线程心跳 |
| 多 MCP 混合分析 | 同一任务混用数据源会造成口径不一致 | 拆成两个独立任务 |
| 无证据的竞品归因 | 数据不够时不能强行判断 | 报告中写“不足以确认” |

---

## 4. 核心原则

### 4.1 一个任务只监控一种对象

每个任务的 `monitor_type` 只能是下面四种之一：

| 类型 | 用法 | 示例 |
| --- | --- | --- |
| `asin` | 监控一个 ASIN | `B0BG63CR3K` |
| `multi-asin` | 监控一组 ASIN | 5 个鸟笼包竞品 |
| `seller` | 监控一个卖家 | 某店铺名 |
| `brand` | 监控一个品牌 | `Anker` |

如果同一个主体既要看品牌，又要看卖家，必须拆成两个任务。

### 4.2 一个任务只使用一个 MCP

每个任务只能使用一种数据源：

| MCP | 推荐场景 | 说明 |
| --- | --- | --- |
| `sellersprite-mcp` | 深度竞品分析、品牌/卖家/关键词/流量结构 | 默认选择，适合绝大多数监控任务 |
| `sorftime_mcp` | 实时商品搜索、轻量商品巡检、榜单趋势 | 更适合当前商品视角，但深度结构分析较弱 |

重要规则：

- 不要在同一任务里同时用 SellerSprite 和 Sorftime。
- 如果中途发现 MCP 不够用，不要临时混用，应该新建第二个任务。
- 报告里必须写清楚本次数据来源 MCP 和口径。

### 4.3 日报、周报、快照、记忆必须分开

每个任务默认有四类输出：

| 文件 / 目录 | 用途 |
| --- | --- |
| `tasks/{task_id}.yaml` | 任务配置 |
| `docs/{task_id}-daily.md` | 日报，按日期追加 |
| `docs/{task_id}-weekly.md` | 周报，按周追加 |
| `snapshots/{task_id}/` | 结构化快照，用来做前后对比 |
| `memory/{task_id}/rolling-memory.md` | 人看的长期记忆 |
| `memory/{task_id}/signal-ledger.jsonl` | 机器读的信号流水 |
| `memory/{task_id}/hypotheses.yaml` | 待验证假设 |

---

## 5. 安装与验证

### 5.1 安装到 Codex

```bash
curl -fsSL https://raw.githubusercontent.com/WaytoAIC/amazon-competitor-monitor/v1.1.1/install.sh | bash -s -- --target codex --ref v1.1.1
```

安装后重启 Codex。

### 5.2 安装到 OpenClaw

```bash
curl -fsSL https://raw.githubusercontent.com/WaytoAIC/amazon-competitor-monitor/v1.1.1/install.sh | bash -s -- --target openclaw --ref v1.1.1
```

安装后重启 OpenClaw。

### 5.3 安装到自定义目录

```bash
curl -fsSL https://raw.githubusercontent.com/WaytoAIC/amazon-competitor-monitor/v1.1.1/install.sh | bash -s -- --dest "$(pwd)/skills" --ref v1.1.1
```

### 5.4 验证是否安装成功

在 Codex 中输入：

```text
用 $amazon-competitor-monitor 帮我说明这个 skill 能做什么
```

如果 Codex 能识别并按竞品监控规则回答，说明 Skill 已经生效。

---

## 6. 工作区结构

建议每个竞品监控项目使用固定结构：

```text
workspace/
├── tasks/
├── docs/
├── snapshots/
├── memory/
└── logs/
```

说明：

| 目录 | 运营理解 |
| --- | --- |
| `tasks/` | 放任务配置。一个监控对象一个 YAML 文件 |
| `docs/` | 放日报和周报，给人阅读 |
| `snapshots/` | 放每次抓取的结构化数据，便于对比 |
| `memory/` | 放长期记忆、信号流水、假设 |
| `logs/` | 放运行记录、失败说明、临时备注 |

---

## 7. 新建监控任务 SOP

### 7.1 新建任务前先确认 6 个信息

| 信息 | 必填 | 示例 |
| --- | --- | --- |
| 任务 ID | 是 | `asin-b0bg63cr3k-us` |
| 站点 | 是 | `US` |
| 监控类型 | 是 | `asin` / `multi-asin` / `seller` / `brand` |
| 监控目标 | 是 | ASIN、ASIN 列表、卖家名或品牌名 |
| MCP | 是 | 默认 `sellersprite-mcp` |
| 输出节奏 | 是 | `daily`、`weekly` 或两者都要 |

### 7.2 用自然语言让 Codex 建任务

推荐运营直接这样说：

```text
用 $amazon-competitor-monitor 帮我在当前目录建一个竞品监控任务：
站点 US
监控类型 asin
目标 B0BG63CR3K
任务 ID asin-b0bg63cr3k-us
只使用 sellersprite-mcp
输出日报和周报
启用盈利模型雷达
```

Codex 应该做的事：

1. 读取 `amazon-competitor-monitor` Skill。
2. 创建工作区目录。
3. 生成 `tasks/{task_id}.yaml`。
4. 生成日报、周报模板。
5. 生成 `memory/{task_id}/` 下的长期记忆文件。
6. 确认任务只使用一个 MCP。

### 7.3 用脚本建任务

如果想直接用命令：

```bash
python3 amazon-competitor-monitor/scripts/init_monitor_workspace.py \
  --workspace "$(pwd)" \
  --task-id asin-b0bg63cr3k-us \
  --monitor-type asin \
  --target B0BG63CR3K \
  --mcp sellersprite-mcp \
  --marketplace US \
  --cadence daily \
  --cadence weekly \
  --priority 80 \
  --radar \
  --focus price,coupon,sales,bsr,rating,review,traffic,keyword \
  --notes "Monitor US ASIN B0BG63CR3K with daily and weekly outputs; use only sellersprite-mcp for this task."
```

脚本会生成：

```text
tasks/asin-b0bg63cr3k-us.yaml
docs/asin-b0bg63cr3k-us-daily.md
docs/asin-b0bg63cr3k-us-weekly.md
snapshots/asin-b0bg63cr3k-us/
memory/asin-b0bg63cr3k-us/rolling-memory.md
memory/asin-b0bg63cr3k-us/signal-ledger.jsonl
memory/asin-b0bg63cr3k-us/hypotheses.yaml
```

### 7.4 常用建任务命令模板

单 ASIN：

```bash
python3 amazon-competitor-monitor/scripts/init_monitor_workspace.py \
  --workspace "$(pwd)" \
  --task-id asin-b0xxxx-us \
  --monitor-type asin \
  --target B0XXXX \
  --mcp sellersprite-mcp \
  --marketplace US \
  --radar
```

多 ASIN：

```bash
python3 amazon-competitor-monitor/scripts/init_monitor_workspace.py \
  --workspace "$(pwd)" \
  --task-id bird-carrier-top5-us \
  --monitor-type multi-asin \
  --target B0AAAA,B0BBBB,B0CCCC,B0DDDD,B0EEEE \
  --mcp sellersprite-mcp \
  --marketplace US \
  --radar
```

卖家：

```bash
python3 amazon-competitor-monitor/scripts/init_monitor_workspace.py \
  --workspace "$(pwd)" \
  --task-id seller-example-us \
  --monitor-type seller \
  --target "SellerName" \
  --mcp sellersprite-mcp \
  --marketplace US \
  --radar
```

品牌：

```bash
python3 amazon-competitor-monitor/scripts/init_monitor_workspace.py \
  --workspace "$(pwd)" \
  --task-id brand-anker-us \
  --monitor-type brand \
  --target Anker \
  --mcp sellersprite-mcp \
  --marketplace US \
  --radar
```

---

## 8. 任务配置字段说明

典型配置如下：

```yaml
task_id: "asin-b0bg63cr3k-us"
enabled: true
priority: 80
marketplace: "US"
monitor_type: "asin"
targets:
  asin: "B0BG63CR3K"
mcp: "sellersprite-mcp"
cadences:
  - "daily"
  - "weekly"
comparison:
  daily_lookback_days: 1
  weekly_lookback_days: 7
outputs:
  daily_doc: "docs/asin-b0bg63cr3k-us-daily.md"
  weekly_doc: "docs/asin-b0bg63cr3k-us-weekly.md"
  snapshot_dir: "snapshots/asin-b0bg63cr3k-us"
memory:
  enabled: true
  recent_daily_reports: 7
  recent_weekly_reports: 4
  signal_confirmation_threshold: 3
  hypothesis_review_cadence: "weekly"
  rolling_memory_doc: "memory/asin-b0bg63cr3k-us/rolling-memory.md"
  signal_ledger: "memory/asin-b0bg63cr3k-us/signal-ledger.jsonl"
  hypotheses_doc: "memory/asin-b0bg63cr3k-us/hypotheses.yaml"
analysis_layers:
  - "monitoring"
  - "profit-model"
  - "strategy-radar"
focus:
  - "price"
  - "coupon"
  - "sales"
  - "bsr"
  - "rating"
  - "review"
  - "traffic"
  - "keyword"
notes: "Monitor US ASIN B0BG63CR3K with daily and weekly outputs; use only sellersprite-mcp for this task."
```

字段解释：

| 字段 | 含义 | 注意事项 |
| --- | --- | --- |
| `task_id` | 任务唯一 ID | 用小写短横线，后续文档都跟它走 |
| `enabled` | 是否启用 | `false` 的任务不执行 |
| `priority` | 优先级 | 多任务时数字越大越先跑 |
| `marketplace` | Amazon 站点 | 例如 `US`、`JP`、`DE` |
| `monitor_type` | 监控类型 | 只能四选一 |
| `targets` | 监控对象 | 必须与监控类型匹配 |
| `mcp` | 数据源 | 一个任务只能一个 |
| `cadences` | 输出节奏 | `daily`、`weekly` |
| `outputs` | 输出路径 | 日报、周报、快照目录 |
| `memory` | 长期记忆设置 | 建议默认开启 |
| `analysis_layers` | 分析层 | 默认 `monitoring`，可加盈利雷达 |
| `focus` | 重点观察维度 | 价格、评论、关键词等 |
| `notes` | 任务备注 | 写清特殊口径和目的 |

---

## 9. 日报执行 SOP

### 9.1 什么时候跑日报

适合每日或每 2-3 天执行一次。重点看短期变化：

- 价格是否变动。
- Coupon 是否出现或消失。
- BSR / 类目排名是否异常。
- 评论是否出现集中负面主题。
- 关键词排名或流量占比是否变化。
- 广告位、自然位是否有明显变化。
- 是否出现新品、断货、下架、变体调整。

### 9.2 日报运行提示词

```text
用 $amazon-competitor-monitor 更新任务 asin-b0bg63cr3k-us 的日报。
要求：
1. 先读取 tasks/asin-b0bg63cr3k-us.yaml
2. 只使用任务配置里的 sellersprite-mcp
3. 先读取 memory/asin-b0bg63cr3k-us 下的长期记忆
4. 和上次快照、最近日报、长期记忆对比
5. 追加写入 docs/asin-b0bg63cr3k-us-daily.md，不要覆盖历史
6. 保存本次结构化快照到 snapshots/asin-b0bg63cr3k-us/
7. 判断本次变化是噪音、延续、异常、趋势反转还是新信号
8. 如有长期信号，更新 signal-ledger 和 hypotheses
```

### 9.3 日报必须输出的内容

| 模块 | 必须回答的问题 |
| --- | --- |
| 执行摘要 | 今天最重要的 3-5 个结论是什么 |
| KPI 快照 | 价格、优惠、评分、排名、评论、流量词等指标有什么变化 |
| 关键变化 | 哪些变化值得运营注意 |
| 风险与动作 | 我方今天要不要调价、调广告、补素材、看评论 |
| 长期记忆影响 | 是否需要把本次变化写入长期记忆 |
| 下一步观察 | 下次重点看什么 |

### 9.4 日报判断标准

| 判断 | 说明 | 是否进长期记忆 |
| --- | --- | --- |
| 噪音 | 小幅波动，没有策略意义 | 通常不进 |
| 延续 | 和历史判断一致 | 可更新已有信号 |
| 异常 | 单次明显偏离历史 | 先标记 `new` 或 `watching` |
| 趋势反转 | 与历史结论相反 | 标记 `reversed`，不要删除旧记录 |
| 新信号 | 以前没出现过且可能影响策略 | 写入 `signal-ledger.jsonl` |

### 9.5 日报验收清单

| 检查项 | 合格标准 |
| --- | --- |
| 是否追加写入 | 新日期分节追加在日报文档里，没有覆盖旧内容 |
| 是否写明日期 | 有运行日期和对比基线日期 |
| 是否写明 MCP | 明确只用了任务配置里的 MCP |
| 是否有证据 | 每个关键判断都有数据或评论证据 |
| 是否有动作 | 不是空泛总结，而是能执行的动作 |
| 是否更新记忆 | 有长期信号时更新 memory，无信号时说明不更新原因 |

---

## 10. 周报执行 SOP

### 10.1 什么时候跑周报

建议每周固定执行一次。周报不只是把 7 天日报合并，而是要回答战略问题：

- 这一周主线变化是什么。
- 哪些 ASIN / 卖家 / 品牌赢了，哪些掉队了。
- 本周变化是短期战术波动，还是结构性变化。
- 哪些长期假设被强化、推翻或降级。
- 下周我方要采取什么打法。

### 10.2 周报运行提示词

```text
用 $amazon-competitor-monitor 更新任务 asin-b0bg63cr3k-us 的周报。
要求：
1. 先读取 tasks/asin-b0bg63cr3k-us.yaml
2. 只使用任务配置里的 sellersprite-mcp
3. 读取 rolling-memory、hypotheses、signal-ledger、最近 7 篇日报和最近周报
4. 对比本周和上周 / 首次观察周
5. 追加写入 docs/asin-b0bg63cr3k-us-weekly.md，不要覆盖历史
6. 输出盈利模型雷达
7. 复盘假设状态，把达到阈值的信号升级
8. 更新 rolling-memory、signal-ledger、hypotheses
```

### 10.3 周报必须输出的内容

| 模块 | 必须回答的问题 |
| --- | --- |
| 本周摘要 | 本周最重要的主线是什么 |
| 对比记分牌 | 谁领先、谁落后，证据是什么 |
| 结构性变化 | 有没有价格带、流量、评论、产品池结构变化 |
| 长期模式更新 | 哪些信号强化、反转、归档 |
| 盈利模型雷达 | 四个效率维度各几分，证据和置信度是什么 |
| 竞品画像 | 对手属于哪类选手，弱点是什么 |
| 假设复盘 | 哪些假设继续观察，哪些确认，哪些推翻 |
| 评论 / 关键词 / 流量主题 | 本周核心主题 |
| 策略地图与下周动作 | 下周怎么打 |

### 10.4 周报策略地图

| 策略 | 适用情况 | 典型动作 |
| --- | --- | --- |
| 田忌赛马 | 对手是巨头或资金型，正面打成本太高 | 避开大词，打长尾词、精准场景、局部弱点 |
| 侧翼包抄 | 对手同体量但正面竞争贵 | 做材质、颜色、套装、场景、人群差异化 |
| 吸血鬼策略 | 对手流量强但转化弱 | Product Targeting 截对手 ASIN，用更强图片和痛点文案承接 |
| 继续观察 | 证据不足 | 明确下周要验证哪些指标 |

### 10.5 周报验收清单

| 检查项 | 合格标准 |
| --- | --- |
| 是否有主线 | 周报不能只是日报拼接 |
| 是否对比历史 | 写明具体对比日期，不只写“较上周” |
| 是否复盘假设 | `hypotheses.yaml` 有状态变化或明确保留原因 |
| 是否更新长期记忆 | `rolling-memory.md` 记录稳定模式和关键拐点 |
| 是否有策略动作 | 下周动作能落到价格、广告、内容、产品、评论或选品 |
| 是否标注置信度 | 供应链效率、资金实力不能写成确定事实 |

---

## 11. 长期记忆 SOP

长期记忆是这个 Skill 的核心。它避免每次分析都从零开始。

### 11.1 三个记忆文件

| 文件 | 给谁用 | 内容 |
| --- | --- | --- |
| `rolling-memory.md` | 人 | 稳定模式、关键拐点、当前判断、待验证问题 |
| `signal-ledger.jsonl` | 机器 / Codex | 每一条重要信号，按 JSONL 追加 |
| `hypotheses.yaml` | 人 + 机器 | 待验证假设、证据次数、反证次数、状态 |

### 11.2 信号生命周期

| 状态 | 含义 |
| --- | --- |
| `new` | 第一次出现 |
| `watching` | 出现多次，但还没达到确认阈值 |
| `confirmed` | 证据累计达到阈值，成为稳定判断 |
| `reversed` | 新证据推翻旧判断 |
| `archived` | 历史上重要，但当前不再影响策略 |

默认确认阈值是 3 次，也就是同类信号至少出现 3 次才建议从 `watching` 升为 `confirmed`。

### 11.3 什么信号应该进记忆

| 应该进 | 不建议进 |
| --- | --- |
| 影响价格、流量、评论、转化、上新、断货、库存代理、雷达评分的变化 | 一次普通小波动 |
| 连续出现，可能形成趋势 | 没有策略意义的指标噪音 |
| 与历史判断相反 | 没有证据的猜测 |
| 需要周报复盘 | 纯描述性信息 |

### 11.4 用脚本更新记忆

```bash
python3 amazon-competitor-monitor/scripts/update_memory.py \
  --workspace "$(pwd)" \
  --task-id asin-b0bg63cr3k-us \
  --date 2026-04-21 \
  --cadence daily \
  --signal-key traffic-concentration-bird-cage \
  --dimension traffic \
  --summary "`bird cage` 流量集中度继续上升，当前占比约 53.2%。" \
  --evidence "SellerSprite traffic_keyword 当前快照显示 `bird cage` 流量占比高于上次快照。" \
  --confidence high \
  --direction support
```

如果新证据推翻旧判断：

```bash
python3 amazon-competitor-monitor/scripts/update_memory.py \
  --workspace "$(pwd)" \
  --task-id asin-b0bg63cr3k-us \
  --cadence weekly \
  --signal-key traffic-concentration-bird-cage \
  --dimension traffic \
  --summary "`bird cage` 流量占比连续下降，不再是绝对主入口。" \
  --evidence "连续三次快照显示该词占比低于 30%。" \
  --confidence medium \
  --direction contradict
```

如果信号不再影响当前策略：

```bash
python3 amazon-competitor-monitor/scripts/update_memory.py \
  --workspace "$(pwd)" \
  --task-id asin-b0bg63cr3k-us \
  --cadence weekly \
  --signal-key old-promotion-event \
  --dimension price \
  --summary "旧促销事件已不再影响当前价格判断。" \
  --evidence "后续 4 周未重复出现。" \
  --confidence medium \
  --direction archive
```

---

## 12. 盈利模型雷达 SOP

盈利模型雷达用于判断“对手为什么能赚钱 / 为什么能打”。

核心框架：

```text
Amazon profit model = traffic efficiency x conversion efficiency x supply-chain efficiency / capital occupation
```

这是策略归因框架，不是精确财务公式。

### 12.1 四个维度

| 维度 | 看什么 | 可用代理指标 | 置信度提醒 |
| --- | --- | --- | --- |
| 流量效率 | 对手是否能低成本拿到精准流量 | 关键词覆盖、自然排名、广告位、流量占比 | 有关键词和流量来源证据可到 `high` |
| 转化效率 | 流量进来后是否更容易成交 | 评分、评论数、Review 内容、价格带、图片/A+ | 有评分、评论、价格共同证据可到 `high` |
| 供应链效率 | 是否可能有成本和交付优势 | 变体复用、上新节奏、价格稳定、断货情况 | 无内部数据默认不超过 `medium` |
| 资金实力 | 是否能承受库存和投放压力 | 库存深度代理、补货节奏、广告覆盖、低价持续时间 | 无库存/广告花费默认不超过 `medium` |

### 12.2 评分规则

| 分数 | 含义 |
| --- | --- |
| 1 | 明显弱势 |
| 2 | 偏弱 |
| 3 | 中性或证据不足 |
| 4 | 明显优势 |
| 5 | 强壁垒 |

每个分数必须附：

- 证据。
- 代理指标说明。
- 置信度：`high`、`medium`、`low`。
- 较上次变化。

不允许只给分数。

### 12.3 竞品画像

| 画像类型 | 典型特征 | 我方打法 |
| --- | --- | --- |
| 流量型选手 | 关键词覆盖强、广告位多、自然位好 | 避开大词，抓长尾和转化弱点 |
| 品牌型选手 | 评分、图片、品牌溢价强 | 打细分人群、服务、功能差异 |
| 工厂型选手 | 价格低、变体多、供应链复用强 | 不盲目跟价，做体验和内容升级 |
| 资金型选手 | 库存深、广告强、低价持续 | 用田忌赛马，避开正面消耗 |
| 均衡型选手 | 四维都强 | 找局部弱点或错位需求 |

---

## 13. 不同监控类型的操作重点

### 13.1 单 ASIN 监控

重点：

- 价格、Coupon、排名、BSR。
- 评论新增主题。
- 流量词和关键词排名。
- 广告/自然入口变化。
- 变体结构。

常用提示词：

```text
用 $amazon-competitor-monitor 更新单 ASIN 任务 asin-b0xxxx-us 的日报。
重点看价格、Coupon、BSR、评论、流量词和广告/自然入口变化。
只使用任务配置里的 MCP，结论要写清楚证据和口径。
```

### 13.2 多 ASIN 监控

重点：

- 谁涨、谁跌、谁促销。
- 谁的评分、评论、销量、价格带更稳。
- 哪个 ASIN 开始抢关键词或自然位。
- 是否出现新的头部或尾部掉队者。

常用提示词：

```text
用 $amazon-competitor-monitor 更新 multi-asin 任务 bird-carrier-top5-us 的周报。
重点输出对比记分牌、赢家/输家、关键词重叠、价格带变化和下周动作。
不要把不同 MCP 的数据混用。
```

### 13.3 卖家监控

重点：

- 商品池是否扩张或收缩。
- 是否上新、下架、断货。
- 主力 SKU 是否换了。
- 价格带和评分带是否变化。

常用提示词：

```text
用 $amazon-competitor-monitor 更新 seller 任务 seller-example-us 的日报。
重点看商品池变化、上新下架、头部 SKU、异常调价和评论风险。
```

### 13.4 品牌监控

重点：

- 品牌头部款是谁。
- 新品节奏是否加快。
- 品牌集中度和类目覆盖是否变化。
- 是否有新价格带或新场景。

常用提示词：

```text
用 $amazon-competitor-monitor 更新 brand 任务 brand-anker-us 的周报。
重点看品牌商品池、头部款、新品节奏、价格带、评论结构、品牌集中度和策略地图。
```

---

## 14. 数据源选择 SOP

### 14.1 默认选择

默认使用 `sellersprite-mcp`，除非任务明显更适合 Sorftime。

### 14.2 选择表

| 需求 | 推荐 MCP |
| --- | --- |
| 深度 ASIN、关键词、流量结构、评论、卖家/品牌分析 | `sellersprite-mcp` |
| 品牌集中度、卖家池、类目结构 | `sellersprite-mcp` |
| 当前商品详情、实时产品列表、轻量榜单巡检 | `sorftime_mcp` |
| 多 ASIN 轻量价格/评分/销量对比 | 两者都可，但任务内只能选一个 |

### 14.3 口径说明模板

如果用 SellerSprite：

```text
本次仅使用 sellersprite-mcp。部分数据为当前快照、近 30 天、月度或滚动窗口口径，因此日报中的变化表述为“相较上次抓取快照”，不写成“昨日精确变化”。
```

如果用 Sorftime：

```text
本次仅使用 sorftime_mcp。报告更偏当前商品巡检和实时产品视角，深度品牌集中度或流量结构结论不足以确认。
```

---

## 15. 报告写作规范

### 15.1 语言

- 报告正文用中文。
- ASIN、品牌名、卖家名、关键词保留原文。
- 状态枚举保留英文：`new`、`watching`、`confirmed`、`reversed`、`archived`。
- 不使用英文模板标题，例如 `Executive Summary`。

### 15.2 证据

每个关键结论必须写证据：

| 不合格写法 | 合格写法 |
| --- | --- |
| 对手流量很强 | 对手当前覆盖 220 个流量词，`bird cage` 占比约 53.2%，`bird carrier` 自然位约第 1，流量效率判断为偏强，置信度 high |
| 对手供应链很强 | 对手有 19 个变体、FBA、价格 16.99 美元，但无内部成本数据，因此供应链效率只能做代理推断，置信度 medium |
| 建议优化广告 | 下周先测试 `bird carrier travel cage`、`travel bird cage` 和 Product Targeting，对 B0BG63CR3K 做小预算截流测试 |

### 15.3 动作建议

动作建议必须具体到可执行：

- 价格动作。
- 广告动作。
- 关键词动作。
- Listing 文案 / 图片动作。
- 评论痛点跟踪。
- 新品或变体跟进。
- 记忆更新动作。
- 假设验证动作。

---

## 16. 质量验收标准

### 16.1 新建任务验收

| 项目 | 合格标准 |
| --- | --- |
| 任务配置 | `tasks/{task_id}.yaml` 存在且字段完整 |
| 监控对象 | `monitor_type` 和 `targets` 匹配 |
| MCP | 只写一个 MCP |
| 输出文件 | 日报、周报路径正确 |
| 记忆文件 | `rolling-memory.md`、`signal-ledger.jsonl`、`hypotheses.yaml` 存在 |
| 雷达 | 需要策略分析时，`analysis_layers` 包含 `profit-model` 和 `strategy-radar` |

### 16.2 日报验收

| 项目 | 合格标准 |
| --- | --- |
| 追加方式 | 在原日报追加新日期分节 |
| 对比基线 | 写清楚对比哪一天或哪次快照 |
| 证据 | 关键变化都有证据 |
| 判断 | 标明噪音 / 延续 / 异常 / 趋势反转 / 新信号 |
| 动作 | 至少 2-3 条具体动作 |
| 记忆 | 应进记忆的信号已更新 |

### 16.3 周报验收

| 项目 | 合格标准 |
| --- | --- |
| 主线 | 有本周主线结论 |
| 记分牌 | 有领先/落后对比 |
| 雷达 | 有四维评分、证据、代理指标、置信度 |
| 假设 | 复盘 `hypotheses.yaml` |
| 记忆 | 更新长期模式和关键拐点 |
| 下周动作 | 有价格、广告、内容、产品或评论跟进动作 |

---

## 17. 常见问题与处理

### 17.1 报告里混用了两个 MCP

处理：

1. 停止继续写报告。
2. 保留已经抓到的数据，但不要作为同一任务结论。
3. 新建第二个任务，专门使用另一个 MCP。
4. 在原任务文档里说明本次混用数据不进入长期记忆。

### 17.2 没有历史快照

写法：

```text
本次为首次建档，暂无可比较历史。以下指标作为后续对比基线，不判断趋势反转。
```

### 17.3 数据是月度或滚动口径

写法：

```text
该指标为 SellerSprite 当前快照 / 近 30 天 / 月度口径，不能解释为昨日精确变化。
```

### 17.4 供应链或资金实力证据不足

写法：

```text
供应链效率只能基于变体数量、价格稳定、履约方式和上新节奏做代理推断，缺少内部成本与库存数据，置信度 medium。
```

### 17.5 结论被新证据推翻

处理：

- 不删除旧结论。
- 在 `signal-ledger.jsonl` 新增一条 `reversed` 记录。
- 在 `rolling-memory.md` 写清楚被推翻的日期和原因。
- 在周报假设复盘里解释。

### 17.6 多任务太多不知道先跑哪个

按 `priority` 从高到低跑：

1. 高优先级核心竞品。
2. 正在对标或正在投放的 ASIN。
3. 新发现的异常竞品。
4. 低优先级品牌/卖家观察任务。

---

## 18. 运营每日使用清单

每天打开工作区后按这个顺序做：

| 步骤 | 动作 | 结果 |
| --- | --- | --- |
| 1 | 查看 `tasks/` 下有哪些 `enabled: true` 任务 | 确认今天要跑哪些 |
| 2 | 按 `priority` 排序 | 高优先级先跑 |
| 3 | 对每个任务运行日报提示词 | 生成当天日报 |
| 4 | 检查日报是否有新信号 | 决定是否进 memory |
| 5 | 保存结构化快照 | 为下一次对比做准备 |
| 6 | 提炼今日动作 | 给广告、Listing、产品或供应链负责人 |

---

## 19. 运营每周使用清单

每周固定一次：

| 步骤 | 动作 | 结果 |
| --- | --- | --- |
| 1 | 读取本周所有日报和快照 | 汇总变化 |
| 2 | 读取 `rolling-memory.md` 和 `hypotheses.yaml` | 知道历史判断 |
| 3 | 生成周报 | 输出主线、雷达、画像和策略 |
| 4 | 复盘假设 | 升级、反转或归档 |
| 5 | 更新长期记忆 | 保留稳定模式和关键拐点 |
| 6 | 形成下周动作清单 | 指导广告、Listing、选品和产品优化 |

---

## 20. 推荐团队分工

| 角色 | 负责内容 |
| --- | --- |
| 运营负责人 | 定义监控对象、判断优先级、确认最终动作 |
| 广告负责人 | 根据关键词、流量、广告位变化调整投放 |
| Listing 负责人 | 根据评论痛点和转化弱点调整图片、标题、五点、A+ |
| 产品 / 供应链负责人 | 根据变体、价格带、评论痛点判断产品改良 |
| Codex 操作员 | 跑任务、维护文档、更新 memory、保证口径一致 |

---

## 21. 可复制提示词合集

### 21.1 建立单 ASIN 任务

```text
用 $amazon-competitor-monitor 在当前目录新建一个单 ASIN 监控任务：
任务 ID：asin-b0xxxx-us
站点：US
目标 ASIN：B0XXXX
MCP：sellersprite-mcp
节奏：daily 和 weekly
启用盈利模型雷达
重点关注 price、coupon、sales、bsr、rating、review、traffic、keyword
要求生成 tasks、docs、snapshots、memory、logs 结构，并说明生成了哪些文件。
```

### 21.2 建立多 ASIN 任务

```text
用 $amazon-competitor-monitor 在当前目录新建一个多 ASIN 竞品监控任务：
任务 ID：top-competitors-us
站点：US
目标 ASIN：B0AAAA、B0BBBB、B0CCCC、B0DDDD、B0EEEE
MCP：sellersprite-mcp
节奏：daily 和 weekly
启用盈利模型雷达
要求一个任务只使用这个 MCP，不混用其他数据源。
```

### 21.3 更新日报

```text
用 $amazon-competitor-monitor 更新任务 asin-b0xxxx-us 的日报。
先读取任务配置和 memory，只使用任务配置里的 MCP。
和上次快照、最近日报、长期记忆对比。
追加写入日报，不覆盖历史。
保存本次快照。
判断每个关键变化是噪音、延续、异常、趋势反转还是新信号。
如有值得长期观察的信号，更新 signal-ledger 和 hypotheses。
```

### 21.4 更新周报

```text
用 $amazon-competitor-monitor 更新任务 asin-b0xxxx-us 的周报。
读取最近 7 篇日报、最近周报、rolling-memory、hypotheses 和 signal-ledger。
输出本周摘要、对比记分牌、结构性变化、长期模式更新、盈利模型雷达、竞品画像、假设复盘和下周动作。
追加写入周报，不覆盖历史。
更新长期记忆。
```

### 21.5 只做竞品盈利模型复盘

```text
用 $amazon-competitor-monitor 基于任务 asin-b0xxxx-us 的历史日报、周报、快照和 memory，单独复盘竞品盈利模型雷达。
四个维度都要给 1-5 分、证据、代理指标、置信度和较上次变化。
供应链效率和资金实力如果证据不足，必须明确写“不足以确认”，不要写成确定事实。
```

---

## 22. 最小可用流程

如果只想先跑起来，按这 5 步：

1. 安装 Skill。
2. 在工作区执行 `init_monitor_workspace.py` 新建任务。
3. 让 Codex 用 `$amazon-competitor-monitor` 更新一次日报。
4. 一周后更新周报。
5. 每次有重要信号时更新 `memory/{task_id}/`。

最小合格结果：

```text
tasks/ 有任务配置
docs/ 有日报和周报
snapshots/ 有结构化快照
memory/ 有长期记忆、信号流水、假设
报告中明确写了数据来源、对比基线、证据、判断和动作
```

---

## 23. 一句话 SOP

新建任务时先定对象和 MCP；每天追加日报看短期变化；每周追加周报看结构变化；重要变化写入长期记忆；任何结论都必须有证据、日期、口径和可执行动作。
