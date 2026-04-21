# 展示卡规则

## 目标

把已经生成的 Amazon 竞品日报或周报压缩成一张适合截图、PPT、飞书或汇报展示的卡片。展示卡是报告的视觉摘要，不替代原始 Markdown 报告。

## 输出文件

每次生成展示卡必须尽量输出一组文件：

| 类型 | 默认命名 |
| --- | --- |
| 日报 HTML | `docs/{task_id}-{date}-daily-card.html` |
| 日报 PNG | `docs/{task_id}-{date}-daily-card.png` |
| 周报 HTML | `docs/{task_id}-{week_label}-weekly-card.html` |
| 周报 PNG | `docs/{task_id}-{week_label}-weekly-card.png` |

如果用户要求沿用旧命名，也可以另存为 `docs/{task_id}-daily-card.html/png` 或 `docs/{task_id}-weekly-card.html/png`，但不要覆盖原始日报 / 周报 Markdown。

## 推荐命令

日报：

```bash
python3 {skill_dir}/scripts/generate_report_card.py \
  --workspace <workspace> \
  --task-id <task_id> \
  --cadence daily \
  --date YYYY-MM-DD \
  --screenshot
```

周报：

```bash
python3 {skill_dir}/scripts/generate_report_card.py \
  --workspace <workspace> \
  --task-id <task_id> \
  --cadence weekly \
  --screenshot
```

可选参数：

| 参数 | 用途 |
| --- | --- |
| `--snapshot <path>` | 指定结构化快照 |
| `--html-out <path>` | 指定 HTML 输出 |
| `--png-out <path>` | 指定 PNG 输出 |
| `--image-url <url>` | 为日报卡补商品图 |
| `--width 1280 --height 820` | 指定截图尺寸 |

## 视觉规则

- HTML 必须是单文件、内联 CSS、无需 CDN。
- PNG 默认使用 1280 x 820，适合直接放入 PPT 或飞书。
- 卡片圆角不超过 8px。
- 卡片保留中文标题、中文表头和中文结论；ASIN、品牌、关键词、MCP 名称和状态枚举保留原文。
- 不要放完整报告正文。卡片只保留一屏内能读完的展示内容。
- 不要使用纯渐变或装饰性背景图；可用浅色网格、清晰分区、KPI、条形图和策略块。
- 颜色要服务信息层级：稳定指标用绿色 / 蓝色，风险和警示用红色 / 琥珀色，普通说明用灰色。

## 内容规则

### 日报卡

必须包含：

- 日期、站点、ASIN
- 一句话主结论
- 关键 KPI：价格、评分、评论 / ratings、销量或流量词
- 2-4 个关键变化
- 1 个最重要动作建议
- 数据来源和口径说明

优先展示：

- 价格 / Coupon 是否变化
- BSR / 类目徽章是否变化
- 核心关键词流量占比、自然排名和广告位
- Review 是否出现新痛点
- 长期记忆状态变化，例如 `new` -> `watching`

### 周报卡

必须包含：

- 周期、站点、ASIN
- 一句话周度主线
- 盈利模型雷达：流量效率、转化效率、供应链效率、资金实力
- 机会与风险矩阵
- 下周策略动作：田忌赛马、侧翼包抄、吸血鬼策略、继续观察中选用适合项
- 数据来源和口径说明

## 证据纪律

- 如果快照来自月度、近 30 天或滚动预测口径，卡片底部必须写明。
- 如果没有真实逐日历史快照，不要写“昨日销量精确变化”。
- 如果供应链效率和资金实力只是代理推断，必须保留置信度。
- 卡片标题可以更展示化，但不能夸大报告结论。
