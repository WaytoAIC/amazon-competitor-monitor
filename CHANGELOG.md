# Changelog

All notable changes to this project will be documented in this file.

The format is intentionally simple and optimized for release notes and repository readers.

## [Unreleased]

## [v1.1.1] - 2026-04-20

### Changed

- Switched daily, weekly, and rolling-memory templates to Chinese section titles and Chinese placeholders
- Strengthened skill and reporting rules so monitor outputs use Chinese by default while preserving ASINs, brand names, seller names, keywords, MCP names, and machine-readable status values
- Updated `update_memory.py` to append Chinese labels in `rolling-memory.md`

## [v1.1.0] - 2026-04-20

### Added

- Long-term task memory with `rolling-memory.md`, `signal-ledger.jsonl`, and `hypotheses.yaml`
- Profit-model radar guidance for traffic efficiency, conversion efficiency, supply-chain efficiency, and capital strength
- `memory-playbook.md` and `profit-model-playbook.md` references
- `--radar` and `--analysis-layer` support in the workspace initializer
- `update_memory.py` helper for repeatable signal lifecycle updates

### Changed

- Daily and weekly report templates now include memory impact, long-term pattern updates, hypotheses, and strategy radar sections
- Task schema now includes `memory` and `analysis_layers` while remaining compatible with v1.0.0 task configs

## [v1.0.0] - 2026-03-27

First public release.

### Added

- Initial `amazon-competitor-monitor` skill
- Support for `asin`, `multi-asin`, `seller`, and `brand` monitoring tasks
- One-task-one-MCP rule with `sellersprite-mcp` default and `sorftime_mcp` option
- Daily and weekly reporting templates
- Workspace bootstrap script for `tasks/`, `docs/`, `snapshots/`, and `logs/`
- Bilingual README, installer, and source-available licensing files
