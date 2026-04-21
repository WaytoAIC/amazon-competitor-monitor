#!/usr/bin/env python3
"""Render Amazon competitor monitor daily/weekly snapshots as HTML + PNG cards."""

import argparse
import html
import json
import shutil
import subprocess
from pathlib import Path


def load_json(path):
    with Path(path).open("r", encoding="utf-8") as fh:
        return json.load(fh)


def pct(value):
    if value is None:
        return "N/A"
    return f"{value * 100:.2f}%"


def safe(value, fallback="N/A"):
    if value in (None, ""):
        return fallback
    return str(value)


def e(value):
    return html.escape(safe(value))


def find_snapshot(workspace, task_id, cadence, date=None, snapshot=None):
    if snapshot:
        return Path(snapshot)
    snap_dir = workspace / "snapshots" / task_id
    if cadence == "daily":
        if not date:
            matches = sorted(snap_dir.glob("*.daily.json"))
            if not matches:
                raise FileNotFoundError(f"No daily snapshots under {snap_dir}")
            return matches[-1]
        return snap_dir / f"{date}.daily.json"

    matches = sorted(snap_dir.glob("*.weekly.json"))
    if not matches:
        raise FileNotFoundError(f"No weekly snapshots under {snap_dir}")
    return matches[-1]


def normalize_week_label(snapshot):
    window = snapshot.get("week_window") or {}
    label = window.get("label") or f"{window.get('start', 'week')}_to_{window.get('end', 'end')}"
    return (
        label.lower()
        .replace(" ", "-")
        .replace("/", "-")
        .replace("_", "-")
        .replace("--", "-")
    )


def metric_card(label, value, note):
    return f"""
          <div class="metric">
            <div class="metric-label">{e(label)}</div>
            <div class="metric-value">{e(value)}</div>
            <div class="metric-note">{e(note)}</div>
          </div>"""


def bar_row(label, width, value, color_class=""):
    width = max(4, min(100, width))
    return f"""
          <div class="bar-row">
            <div class="bar-label">{e(label)}</div>
            <div class="bar-track"><div class="bar-fill {color_class}" style="width: {width:.2f}%"></div></div>
            <div class="bar-value">{e(value)}</div>
          </div>"""


def daily_html(snapshot, args, out_name):
    product = snapshot.get("product", {})
    traffic = snapshot.get("traffic", {})
    terms = traffic.get("top_keywords_by_traffic", [])
    first = terms[0] if terms else {}
    second = terms[1] if len(terms) > 1 else {}
    date = args.date or snapshot.get("collected_at", "")[:10] or "daily"
    price = product.get("price")
    rating = product.get("rating")
    ratings = product.get("ratings")
    total_keywords = traffic.get("total_keywords")
    category_rank = product.get("sub_category_rank")
    image = args.image_url or product.get("image_url") or ""
    asin = snapshot.get("asin") or args.task_id
    marketplace = snapshot.get("marketplace", "")
    source = snapshot.get("source_mcp", "")
    title = "长尾词位次强化，泛词流量更集中"
    if first.get("keyword") and first.get("traffic_percentage") is not None:
        title = f"{first['keyword']} 占比 {pct(first['traffic_percentage'])}，长尾词继续观察"
    if second.get("keyword") and second.get("natural_position") == 1:
        title = f"{second['keyword']} 自然第 1，{first.get('keyword', '核心词')} 流量更集中"

    image_block = (
        f'<img src="{html.escape(image)}" alt="{e(asin)} product image">'
        if image
        else f'<div class="image-fallback">{e(asin)}</div>'
    )

    keyword_rows = []
    for idx, term in enumerate(terms[:5]):
        value = pct(term.get("traffic_percentage"))
        width = (term.get("traffic_percentage") or 0) * 100
        if term.get("natural_position") == 1:
            value = "自然 #1"
            width = 42
        keyword_rows.append(bar_row(term.get("keyword", "-"), width, value, ["", "blue", "", "amber", ""][idx] if idx < 5 else ""))

    long_tails = traffic.get("priority_long_tail_terms", [])
    long_tail_text = "、".join(
        f"{item.get('keyword')} 自然#{item.get('natural_position')}"
        for item in long_tails[:3]
        if item.get("keyword")
    ) or "暂无新增长尾证据"

    core_term = first.get("keyword", "核心词")
    second_term = second.get("keyword", "精准长尾")
    core_change = ""
    if first.get("traffic_percentage") is not None and first.get("previous_traffic_percentage") is not None:
        delta = (first["traffic_percentage"] - first["previous_traffic_percentage"]) * 100
        core_change = f"较上次 {delta:+.2f} 个百分点"

    second_change = ""
    if second.get("natural_position") and second.get("previous_natural_position"):
        second_change = f"自然位从第 {second['previous_natural_position']} 到第 {second['natural_position']}"

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(asin)} 日报展示卡</title>
  <style>{CARD_CSS}</style>
</head>
<body class="daily">
  <main class="card" aria-label="{e(asin)} 日报展示卡">
    <header class="header">
      <div>
        <div class="eyebrow"><span class="dot"></span>ASIN 日报 · {e(date)} · {e(marketplace)}</div>
        <h1>{e(asin)}：{e(title)}</h1>
        <p class="sub">价格、评分、变体和类目位置用于判断基本盘；关键词排名、流量占比和 Review 主题用于判断当日变化是否进入长期记忆。</p>
      </div>
      <aside class="product">
        {image_block}
        <div>
          <div class="product-name">{e(product.get("brand", ""))} · {e(asin)}</div>
          <div class="badges">
            <span class="badge">#{e(category_rank)} Bird Carriers</span>
            <span class="badge">{e(product.get("fulfillment", "FBA"))}</span>
            <span class="badge">{e(product.get("variations", "-"))} 变体</span>
          </div>
        </div>
      </aside>
    </header>
    <section class="content">
      <div class="section">
        <h2>KPI 快照</h2>
        <div class="metrics">
          {metric_card("价格", f"${price:.2f}" if isinstance(price, (int, float)) else safe(price), "Coupon: " + ("无" if not product.get("coupon") else product.get("coupon")))}
          {metric_card("评分 / Ratings", f"{rating} / {ratings}", f"Review 口径 {safe(product.get('reviews_page_total', product.get('reviews_detail')))}")}
          {metric_card("月销量预测", safe(snapshot.get("sales_proxy", {}).get("monthly_units_estimate")), "SellerSprite 月度/滚动口径")}
          {metric_card("流量词", safe(total_keywords), f"广告相关 {safe(traffic.get('ad_keywords'))}")}
        </div>
      </div>
      <div class="section wide">
        <h2>关键词位势</h2>
        <div class="bar-list">
          {''.join(keyword_rows)}
        </div>
      </div>
      <div class="section wide">
        <h2>关键变化</h2>
        <div class="change-list">
          <div class="change"><div class="icon red">1</div><div><div class="change-title">{e(core_term)} 流量集中</div><div class="change-text">当前占比 {pct(first.get("traffic_percentage"))}；{e(core_change or "等待下一次快照验证")}。</div></div></div>
          <div class="change"><div class="icon blue">2</div><div><div class="change-title">{e(second_term)} 长尾承接</div><div class="change-text">{e(second_change or "自然 / 广告位置维持观察")}；广告位 {e(second.get("ad_position", "-"))}。</div></div></div>
          <div class="change"><div class="icon amber">3</div><div><div class="change-title">Travel 场景词</div><div class="change-text">{e(long_tail_text)}。</div></div></div>
        </div>
      </div>
      <div class="section">
        <h2>展示结论</h2>
        <div class="action">不要只拼核心 exact bid。优先用 Product Targeting 和安全 / 低味 / 尺寸清楚等差异点承接竞品流量。</div>
      </div>
    </section>
    <footer class="footer"><span>数据源：{e(source)}</span><span>文件：{e(out_name)} · 口径：当前快照 + 月度/滚动预测</span></footer>
  </main>
</body>
</html>
"""


def score_row(label, data, color_class=""):
    score = data.get("score", 3)
    confidence = data.get("confidence", "low")
    return f"""
          <div class="radar-row">
            <div class="radar-label">{e(label)}</div>
            <div class="track"><div class="fill {color_class}" style="width: {min(100, max(20, score * 20))}%"></div></div>
            <div class="score">{e(score)}/5</div>
            <div class="confidence {e(confidence)}">{e(confidence)}</div>
          </div>"""


def weekly_html(snapshot, args, out_name):
    asin = snapshot.get("asin") or args.task_id
    marketplace = snapshot.get("marketplace", "")
    source = snapshot.get("source_mcp", "")
    window = snapshot.get("week_window", {})
    start = window.get("start", "")
    end = window.get("end", "")
    scorecard = snapshot.get("scorecard", {})
    headline = snapshot.get("headline") or "流量 + 转化型细分类目头部，打法应避开泛词硬拼"
    strategies = snapshot.get("strategy", [])
    strategy_rows = "".join(
        f'<div class="strategy-row"><div class="strategy-name">{e(item.split("：", 1)[0])}</div><div>{e(item.split("：", 1)[1] if "：" in item else item)}</div></div>'
        for item in strategies[:3]
    )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(asin)} 周报展示卡</title>
  <style>{CARD_CSS}</style>
</head>
<body class="weekly">
  <main class="card" aria-label="{e(asin)} 周报展示卡">
    <header class="header">
      <div>
        <div class="eyebrow"><span class="dot"></span>ASIN 周报 · {e(start)} 至 {e(end)} · {e(marketplace)}</div>
        <h1>{e(headline)}</h1>
        <p class="sub">周报卡聚焦主线判断、盈利模型雷达、机会风险和下周动作。若没有真实逐日历史快照，底部必须保留口径说明。</p>
      </div>
      <aside class="hero-kpi">
        <div class="hero-row"><span class="hero-label">周期</span><span class="hero-value">{e(window.get("label", "weekly"))}</span></div>
        <div class="hero-row"><span class="hero-label">ASIN</span><span class="hero-value">{e(asin)}</span></div>
        <div class="hero-row"><span class="hero-label">数据源</span><span class="hero-value">{e(source)}</span></div>
      </aside>
    </header>
    <section class="content">
      <div class="section">
        <h2>盈利模型雷达</h2>
        <div class="radar">
          {score_row("流量效率", scorecard.get("traffic_efficiency", {}), "")}
          {score_row("转化效率", scorecard.get("conversion_efficiency", {}), "green")}
          {score_row("供应链", scorecard.get("supply_chain_efficiency", {}), "amber")}
          {score_row("资金实力", scorecard.get("capital_strength", {}), "purple")}
        </div>
      </div>
      <div class="section">
        <h2>周度主线</h2>
        <div class="story">
          <div class="story-item"><div class="story-tag">头部位置</div><div class="story-title">类目锚点</div><div class="story-text">优先判断徽章、BSR、评分和变体是否继续支撑头部位置。</div></div>
          <div class="story-item"><div class="story-tag amber">流量结构</div><div class="story-title">泛词 + 长尾</div><div class="story-text">观察核心词集中度，同时确认精准词是否形成自然和广告双防守。</div></div>
          <div class="story-item"><div class="story-tag blue">转化缺口</div><div class="story-title">评论痛点</div><div class="story-text">安全、异味、拉链、尺寸等痛点可转为差异化卖点。</div></div>
        </div>
      </div>
      <div class="section">
        <h2>机会与风险矩阵</h2>
        <div class="matrix">
          <div class="matrix-row"><div class="matrix-key">对手优势</div><div class="matrix-value">{e(scorecard.get("traffic_efficiency", {}).get("evidence", "关键词覆盖、自然排名和广告位是主要优势。"))}</div></div>
          <div class="matrix-row"><div class="matrix-key">可打弱点</div><div class="matrix-value">{e(scorecard.get("conversion_efficiency", {}).get("evidence", "负评主题可作为差异化入口。"))}</div></div>
          <div class="matrix-row"><div class="matrix-key">监控信号</div><div class="matrix-value">{e("、".join(snapshot.get("memory_updates", [])) or "等待后续信号沉淀")}</div></div>
        </div>
      </div>
      <div class="section">
        <h2>下周动作</h2>
        <div class="strategy">{strategy_rows}</div>
      </div>
    </section>
    <footer class="footer"><span>数据源：{e(source)} · 单一 MCP 口径</span><span>{e(snapshot.get("data_scope_note", "口径：当前快照 + 月度/滚动预测"))} · 文件：{e(out_name)}</span></footer>
  </main>
</body>
</html>
"""


CARD_CSS = r"""
:root{color-scheme:light;--ink:#172026;--muted:#65717a;--line:#d9e1e5;--panel:#fff;--page:#f3f6f4;--teal:#0b6b65;--green:#1f8a5b;--amber:#c17400;--red:#c44c3b;--blue:#2f63b7;--purple:#6d579f;--soft-teal:#e4f3ef;--soft-amber:#fff1d7;--soft-red:#fde8e3;--soft-blue:#e8effb}*{box-sizing:border-box}body{margin:0;min-height:100vh;display:grid;place-items:center;padding:28px;background:linear-gradient(90deg,rgba(11,107,101,.06) 1px,transparent 1px),linear-gradient(0deg,rgba(11,107,101,.05) 1px,transparent 1px),var(--page);background-size:32px 32px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",Arial,sans-serif;color:var(--ink)}body.weekly{background:linear-gradient(90deg,rgba(193,116,0,.07) 1px,transparent 1px),linear-gradient(0deg,rgba(11,107,101,.05) 1px,transparent 1px),#f5f3ef;background-size:34px 34px}.card{width:min(1180px,100%);min-height:664px;background:var(--panel);border:1px solid var(--line);border-radius:8px;box-shadow:0 22px 55px rgba(23,32,38,.12);overflow:hidden}.header{display:grid;grid-template-columns:1.35fr .65fr;gap:24px;padding:28px 32px 20px;border-bottom:1px solid var(--line);background:linear-gradient(180deg,#fff 0%,#f8fbfa 100%)}.eyebrow{display:flex;align-items:center;gap:10px;color:var(--teal);font-size:13px;font-weight:800;letter-spacing:0;text-transform:uppercase}body.weekly .eyebrow{color:var(--amber)}.dot{width:10px;height:10px;border-radius:50%;background:var(--green);box-shadow:0 0 0 5px rgba(31,138,91,.12)}body.weekly .dot{background:var(--amber);box-shadow:0 0 0 5px rgba(193,116,0,.14)}h1{margin:10px 0;font-size:32px;line-height:1.16;letter-spacing:0}.sub{max-width:780px;margin:0;color:var(--muted);font-size:15px;line-height:1.65}.product{display:grid;grid-template-columns:104px 1fr;gap:16px;align-items:center;justify-self:end;width:min(390px,100%);padding:12px;border:1px solid var(--line);border-radius:8px;background:#fff}.product img,.image-fallback{width:104px;height:104px;object-fit:contain;border-radius:6px;background:#f4f6f7}.image-fallback{display:grid;place-items:center;padding:8px;text-align:center;font-size:13px;font-weight:850;color:var(--teal)}.product-name{font-weight:850;line-height:1.3;margin-bottom:8px}.badges{display:flex;flex-wrap:wrap;gap:6px}.badge{display:inline-flex;align-items:center;min-height:22px;padding:2px 8px;border-radius:999px;font-size:12px;font-weight:800;color:var(--teal);background:var(--soft-teal);white-space:nowrap}.hero-kpi{align-self:stretch;display:grid;gap:10px;padding:14px;border:1px solid var(--line);border-radius:8px;background:#fff}.hero-row{display:grid;grid-template-columns:1fr auto;gap:14px;align-items:baseline;padding-bottom:10px;border-bottom:1px solid var(--line)}.hero-row:last-child{padding-bottom:0;border-bottom:0}.hero-label{color:var(--muted);font-size:13px}.hero-value{font-size:22px;font-weight:850}.content{display:grid;grid-template-columns:1fr 1fr 1fr;gap:18px;padding:22px 32px 28px}body.weekly .content{grid-template-columns:1.05fr .95fr}.section{border:1px solid var(--line);border-radius:8px;background:#fff;padding:18px}.section.wide{grid-column:span 2}.section h2{margin:0 0 14px;font-size:16px;line-height:1.3}.metrics{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.metric{min-height:86px;padding:12px;border:1px solid var(--line);border-radius:8px;background:#fbfcfd}.metric-label{color:var(--muted);font-size:12px;margin-bottom:7px}.metric-value{font-size:25px;line-height:1;font-weight:850}.metric-note{margin-top:7px;color:var(--muted);font-size:12px;line-height:1.35}.bar-list,.change-list,.radar,.matrix,.strategy{display:grid;gap:12px}.bar-row{display:grid;grid-template-columns:160px 1fr 72px;align-items:center;gap:12px;font-size:13px}.bar-label{font-weight:800;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.bar-track,.track{height:12px;border-radius:999px;background:#edf2f4;overflow:hidden}.bar-fill,.fill{height:100%;border-radius:999px;background:var(--teal)}.blue{background:var(--blue)}.amber{background:var(--amber)}.green{background:var(--green)}.purple{background:var(--purple)}.bar-value{text-align:right;color:var(--muted);font-weight:800}.change{display:grid;grid-template-columns:34px 1fr;gap:10px;align-items:start}.icon{width:28px;height:28px;display:grid;place-items:center;border-radius:7px;font-weight:900;color:#fff;background:var(--teal)}.icon.red{background:var(--red)}.icon.amber{background:var(--amber)}.icon.blue{background:var(--blue)}.change-title{font-weight:850;margin-bottom:3px}.change-text{color:var(--muted);line-height:1.45;font-size:13px}.action{padding:14px;border-left:4px solid var(--red);background:var(--soft-red);border-radius:6px;line-height:1.55;font-size:14px}.radar-row{display:grid;grid-template-columns:92px 1fr 44px 64px;align-items:center;gap:10px;font-size:13px}.radar-label{font-weight:850}.score{text-align:right;font-weight:850}.confidence{padding:2px 8px;border-radius:999px;background:var(--soft-teal);color:var(--teal);font-size:12px;text-align:center;font-weight:800}.confidence.medium{background:var(--soft-amber);color:var(--amber)}.confidence.low{background:var(--soft-red);color:var(--red)}.story{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.story-item{min-height:130px;padding:14px;border:1px solid var(--line);border-radius:8px;background:#fbfcfd}.story-tag{display:inline-flex;min-height:22px;align-items:center;padding:2px 8px;margin-bottom:10px;border-radius:999px;color:#fff;background:var(--teal);font-size:12px;font-weight:800}.story-tag.amber{background:var(--amber)}.story-tag.blue{background:var(--blue)}.story-title{font-size:14px;font-weight:850;margin-bottom:7px;line-height:1.35}.story-text{color:var(--muted);font-size:13px;line-height:1.45}.matrix-row{display:grid;grid-template-columns:104px 1fr;gap:12px;align-items:start;padding:11px 12px;border-radius:8px;background:#fbfcfd;border:1px solid var(--line)}.matrix-key{font-weight:850;color:var(--teal)}.matrix-value{color:var(--muted);line-height:1.45;font-size:13px}.strategy-row{display:grid;grid-template-columns:112px 1fr;gap:12px;padding:12px;border-left:4px solid var(--blue);background:var(--soft-blue);border-radius:6px;line-height:1.45;font-size:13px}.strategy-row:nth-child(2){border-left-color:var(--green);background:var(--soft-teal)}.strategy-row:nth-child(3){border-left-color:var(--red);background:var(--soft-red)}.strategy-name{font-weight:850}.footer{display:flex;justify-content:space-between;gap:16px;padding:14px 32px 20px;color:var(--muted);font-size:12px;border-top:1px solid var(--line);background:#fbfcfd}@media(max-width:980px){body{padding:16px}.header,.content,body.weekly .content{grid-template-columns:1fr}.product{justify-self:stretch}.section.wide{grid-column:span 1}h1{font-size:28px}.story{grid-template-columns:1fr}.bar-row{grid-template-columns:126px 1fr 58px}.footer{flex-direction:column}}@media print{body{padding:0;background:#fff}.card{width:100%;min-height:auto;box-shadow:none;border:none}}
"""


def write_png(html_path, png_path, width, height):
    chrome = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    mac_chrome = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    if not chrome and mac_chrome.exists():
        chrome = str(mac_chrome)
    if not chrome:
        raise RuntimeError("Chrome/Chromium not found; HTML was generated but PNG cannot be rendered.")
    cmd = [
        chrome,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        f"--window-size={width},{height}",
        f"--screenshot={png_path}",
        Path(html_path).resolve().as_uri(),
    ]
    subprocess.run(cmd, check=True)


def parse_args():
    parser = argparse.ArgumentParser(description="Generate monitor report display cards as HTML and PNG.")
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--cadence", required=True, choices=("daily", "weekly"))
    parser.add_argument("--date", help="Daily date, e.g. 2026-04-21")
    parser.add_argument("--snapshot")
    parser.add_argument("--html-out")
    parser.add_argument("--png-out")
    parser.add_argument("--image-url")
    parser.add_argument("--screenshot", action="store_true", help="Render PNG with local Chrome/Chromium")
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=820)
    return parser.parse_args()


def main():
    args = parse_args()
    workspace = Path(args.workspace).resolve()
    snapshot_path = find_snapshot(workspace, args.task_id, args.cadence, args.date, args.snapshot)
    snapshot = load_json(snapshot_path)
    output_dir = workspace / "docs"
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.cadence == "daily":
        date = args.date or snapshot.get("collected_at", "")[:10] or "latest"
        default_name = f"{args.task_id}-{date}-daily-card"
        html_text = daily_html(snapshot, args, f"{default_name}.html")
    else:
        week_label = normalize_week_label(snapshot)
        default_name = f"{args.task_id}-{week_label}-weekly-card"
        html_text = weekly_html(snapshot, args, f"{default_name}.html")

    html_out = Path(args.html_out) if args.html_out else output_dir / f"{default_name}.html"
    png_out = Path(args.png_out) if args.png_out else output_dir / f"{default_name}.png"
    html_out.parent.mkdir(parents=True, exist_ok=True)
    html_out.write_text(html_text, encoding="utf-8")
    print(f"HTML: {html_out}")

    if args.screenshot:
        write_png(html_out, png_out, args.width, args.height)
        print(f"PNG: {png_out}")


if __name__ == "__main__":
    main()
