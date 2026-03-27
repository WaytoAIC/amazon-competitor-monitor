---
name: amazon-competitor-monitor
description: Build and operate Amazon competitor monitoring workflows for single ASIN, multi-ASIN, seller, or brand tracking with daily and weekly outputs. Use when Codex needs to scaffold or maintain recurring Amazon competitor watch tasks, keep separate report documents per task, choose exactly one MCP per task (default sellersprite-mcp, optional sorftime_mcp), or turn marketplace data into Chinese-first monitoring reports and action lists.
---

# Amazon 竞品监控 Skill

## Overview

为 Amazon 竞品监控提供一套可复用的任务配置、MCP 选型、日报/周报输出和工作区组织方式。它适合从零搭建监控方案，也适合在现有工作区里持续维护多个独立的竞品监控任务。

## 先读哪些文件

按需读取同目录资源：

- `references/task-schema.md`
  - 创建或修改任务配置时必读
- `references/tool-mapping.md`
  - 选择 MCP、确定抓数范围和指标时必读
- `references/reporting-playbook.md`
  - 生成或更新日报/周报时必读
- `assets/task-config.template.yaml`
  - 复制为新任务配置的起点
- `assets/daily-report.template.md`
  - 初始化日报文档时使用
- `assets/weekly-report.template.md`
  - 初始化周报文档时使用
- `scripts/init_monitor_workspace.py`
  - 初始化监控工作区或创建单个监控任务时优先使用

## 不可打破的约束

- 一个监控任务只允许一种监控对象：
  - `asin`
  - `multi-asin`
  - `seller`
  - `brand`
- 一个监控任务只允许一个 MCP：
  - 默认 `sellersprite-mcp`
  - 备选 `sorftime_mcp`
- 不要在同一个任务、同一份报告、同一段结论里混用两个 MCP 的数据。
- 一个任务对应一组固定输出文档；不要把多个任务写进同一份日报或周报。
- 日报只更新 `outputs.daily_doc`；周报只更新 `outputs.weekly_doc`。
- 每次输出都写清楚：
  - 运行日期
  - 对比基线日期
  - 数据来源 MCP
  - 市场站点
- 如果数据源只能提供月度或阶段性指标，不要伪装成“昨日精确变化”；应明确写成“相较上次抓取快照的变化”或“本月口径”。

## 任务工作流

### 1. 先判断是“建任务”还是“跑任务”

如果用户还没有任务配置，或只给了模糊目标，例如：

- “帮我做一个 Anker 品牌监控”
- “帮我盯 5 个竞品 ASIN”
- “我要做卖家日报”

则先创建任务配置，不要直接抓数。

优先方式：

- 运行 `python3 {baseDir}/scripts/init_monitor_workspace.py --workspace <path> ...`
- 或复制 `assets/task-config.template.yaml`

### 2. 读取任务配置

至少确认这些字段：

- `task_id`
- `enabled`
- `priority`
- `marketplace`
- `monitor_type`
- `targets`
- `mcp`
- `cadences`
- `outputs`
- `focus`

缺字段时先补齐，再执行抓数。

### 3. 只按该任务允许的 MCP 抓数

默认使用 `sellersprite-mcp`。

只有当任务配置明确写成 `sorftime_mcp`，或用户明确要求切换时，才使用 `sorftime_mcp`。

如果执行中发现当前 MCP 不够用：

- 不要临时混入另一个 MCP
- 应回到任务配置，提示用户把整个任务切换到另一个 MCP
- 或拆成第二个独立任务

### 4. 按监控类型组织分析

- `asin`
  - 关注单个 ASIN 的价格、Coupon、销量或排名趋势、评论、流量词、广告与自然流量结构
- `multi-asin`
  - 关注一组 ASIN 的对比表、头尾部变化、价格带、评分差、流量词重叠与赢家/输家
- `seller`
  - 关注卖家名下商品池、上新或下架、头部 SKU、价格和评分结构、异常波动
- `brand`
  - 关注品牌商品池、头部款变化、品牌集中度、价格带、口碑结构、上新节奏

具体工具组合不要凭空发明，回到 `references/tool-mapping.md` 选择。

### 5. 生成并更新文档

每次运行只更新当前 cadence 对应的文档：

- `daily` -> `outputs.daily_doc`
- `weekly` -> `outputs.weekly_doc`

更新方式：

- 采用“追加一个新日期分节”的方式，不覆盖历史记录
- 先写摘要，再写证据表，再写动作建议
- 如果有上次快照或上次报告，必须做差异说明
- 如果没有可比基线，明确写“首次建档”或“暂无可比较历史”

### 6. 多任务并行时的顺序

如果一个工作区里有多个任务：

- 只处理 `enabled: true` 的任务
- 按 `priority` 从高到低处理
- 每个任务独立读取配置、抓数、写文档
- 不因为目标相似就合并报告
- 如果用户需要总览，单独生成 master summary，不要塞回各任务文档

## 输出要求

- 中文为主
- ASIN、品牌名、卖家名、关键词保留原文
- 表格优先，尤其是：
  - KPI 快照
  - 变化点
  - 竞品对比
  - 风险与动作
- 判断必须带证据来源或口径说明
- 证据不足时明确写“不足以确认”
- 建议必须面向执行，不要只给泛泛概念

## 何时继续读取 references

遇到以下情况时，不要只依赖本文件，继续打开对应 references：

- 新建任务或修改任务字段
  - 读取 `references/task-schema.md`
- 不确定该用哪个 MCP 或哪些工具
  - 读取 `references/tool-mapping.md`
- 需要正式生成日报或周报结构
  - 读取 `references/reporting-playbook.md`
