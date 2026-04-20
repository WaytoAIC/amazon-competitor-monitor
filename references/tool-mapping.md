# Tool Mapping

## Selection Rule

先做这个判断：

1. 默认选 `sellersprite-mcp`
2. 只有当任务更偏“实时商品搜索、类目榜单、轻量卖家/品牌扫描”时再选 `sorftime_mcp`
3. 一旦选定，就不要在该任务里混用另一个 MCP

## MCP Choice Heuristics

| Situation | Preferred MCP | Why |
| --- | --- | --- |
| 需要更丰富的品牌、卖家、关键词、流量和竞争结构分析 | `sellersprite-mcp` | 工具面更全，适合做深度竞品监控 |
| 需要更偏实时的商品列表、趋势和评论巡检 | `sorftime_mcp` | 商品检索和实时产品视角更直接 |
| 需要品牌集中度、卖家池、流量结构这类深指标 | `sellersprite-mcp` | `sorftime_mcp` 不适合作为单任务唯一数据源完成这些结论 |
| 需要多个 ASIN 的轻量对比和当前榜单位置巡检 | `sorftime_mcp` 或 `sellersprite-mcp` | 看任务重点；若要更深关键词或流量分析，仍优先 `sellersprite-mcp` |

## Sellersprite Playbook

### `asin`

优先组合：

- `asin_detail_with_coupon_trend`
- `asin_prediction`
- `keepa_info`
- `traffic_keyword_stat`
- `traffic_source`
- `review`

适合回答：

- 这个 ASIN 最近有没有价格或 Coupon 变化
- 销量、价格、BSR 和评论趋势是否异常
- 流量更依赖自然还是广告
- 新评论里有没有集中吐槽或卖点变化

### `multi-asin`

优先组合：

- `competitor_lookup` with `asins`
- `traffic_listing`
- `traffic_extend` 或 `keyword_order`
- 必要时对关键 ASIN 单独补 `asin_prediction`

适合回答：

- 一组竞品里谁在拉开差距
- 哪些 ASIN 在价格、评分、销量上领先或掉队
- 谁的流量词覆盖更强
- 是否出现了新的头部或尾部掉队者

### `seller`

优先组合：

- `competitor_lookup` with `sellerName`
- `product_research` 作为补充筛查

适合回答：

- 卖家名下有哪些主力商品
- 是否有上新、下架或明显调价
- 该卖家商品池的评分、销量和价格结构如何变化

### `brand`

优先组合：

- `competitor_lookup` with `brand`
- `market_brand_concentration` when category or `nodeIdPath` is known
- 必要时补 `keyword_research` 或 `keyword_miner`

适合回答：

- 品牌商品池是否扩张
- 头部款是否更集中
- 品牌是否在某个类目形成更高集中度
- 是否出现新的高潜或弱势款

## Sorftime Playbook

### `asin`

优先组合：

- `product_detail`
- `product_report`
- `product_trend`
- `product_reviews`
- `product_traffic_terms`

适合回答：

- 当前产品详情、价格、评分和销量趋势
- 最近评论情绪和关键词曝光变化

### `multi-asin`

优先组合：

- `product_detail` 或 `product_report` for each ASIN
- `product_search` 用于补商品池对照

适合回答：

- 多个 ASIN 的当前价格、评分、销量对照
- 轻量化的赢家和输家比较

### `seller`

优先组合：

- `product_search` with `seller_name`
- `product_report` for the top SKUs

适合回答：

- 指定卖家当前在卖什么
- 哪些 SKU 排名、价格或销量表现最强

### `brand`

优先组合：

- `product_search` with `brand`
- `category_report` or `category_trend` only when the task is category-centric and still stays within Sorftime

适合回答：

- 品牌当前产品池
- 热卖款和价格带变化
- 轻量化的类目位置巡检

## Daily vs Weekly Caveats

- `sellersprite-mcp` 的很多数据是月度、滚动窗口或近似口径。
  - 用它做日报时，应表达为“相较上次抓取快照的变化”
  - 不要写成“昨日销量精确变化”，除非工具明确提供该口径
- `sorftime_mcp` 更适合做实时商品巡检，但深度品牌或流量结构分析较弱。
- 如果日报需要“实时巡检”，周报需要“深度流量结构”，不要在一个任务里混用两个 MCP。
  - 应拆成两个任务
  - 或统一降到一个 MCP 能稳定支持的分析深度

## Minimum Output Pack

每次监控至少确保拿到这些信息：

| Monitor type | Minimum pack |
| --- | --- |
| `asin` | 价格/优惠、趋势、评论摘要、流量结构或曝光关键词 |
| `multi-asin` | 对比表、头部与尾部变化、至少 3 个最重要差异点 |
| `seller` | 商品池列表、主力 SKU、上新/下架、价格或评分变化 |
| `brand` | 品牌商品池、头部款、价格带、口碑结构、上新节奏 |

如果当前 MCP 拿不到最低输出包中的关键证据，应在报告中明确写出能力边界，不要假设或脑补。

## Profit Model Radar Mapping

当任务启用 `profit-model` 或 `strategy-radar` 时，仍然遵守单任务单 MCP 规则。不要为了补齐雷达维度临时混用另一个 MCP。

| Radar Dimension | Sellersprite Proxies | Sorftime Proxies | Confidence Rule |
| --- | --- | --- | --- |
| 流量效率 | `traffic_keyword_stat`、`traffic_source`、`traffic_extend`、`keyword_order`、关键词排名和流量占比 | 商品流量词、商品搜索表现、商品榜单位置 | 有关键词和流量来源证据可到 `high` |
| 转化效率 | 评分、评论数、Review 内容、价格带、Coupon、Listing 质量 | 评分、评论、价格、商品详情和趋势 | 有 Review 与价格/评分共同证据可到 `high` |
| 供应链效率 | 上新节奏、变体结构、品类聚焦、价格带稳定性、断货或 BSR 波动 | 商品池、上新、价格趋势、类目趋势 | 默认不超过 `medium`，除非用户补内部供应链数据 |
| 资金实力 | 库存深度代理、低价持续时间、补货节奏、广告覆盖、产品矩阵 | 商品池深度、榜单持续性、价格策略 | 默认不超过 `medium`，除非用户补库存和资金数据 |

雷达输出必须写：

- 分数：1-5
- 证据：具体指标和日期口径
- 代理指标：说明为什么该指标能代表对应维度
- 置信度：`high`、`medium`、`low`

如果证据不足，评分默认为 3，并写“不足以确认”。
