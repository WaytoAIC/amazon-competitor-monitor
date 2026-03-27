#!/usr/bin/env python3
"""Initialize an Amazon competitor monitoring workspace and task files."""

import argparse
import re
import sys
from pathlib import Path

VALID_MONITOR_TYPES = {"asin", "multi-asin", "seller", "brand"}
VALID_MCPS = {"sellersprite-mcp", "sorftime_mcp"}
VALID_CADENCES = ("daily", "weekly")
DEFAULT_FOCUS = ["price", "coupon", "sales", "rating", "review", "keyword", "traffic"]


def slugify(value):
    normalized = re.sub(r"[^a-z0-9]+", "-", value.strip().lower())
    normalized = re.sub(r"-{2,}", "-", normalized).strip("-")
    return normalized


def split_csv(values):
    items = []
    for value in values or []:
        for part in value.split(","):
            item = part.strip()
            if item and item not in items:
                items.append(item)
    return items


def ensure_dirs(workspace):
    created = []
    for name in ("tasks", "docs", "snapshots", "logs"):
        path = workspace / name
        existed = path.exists()
        path.mkdir(parents=True, exist_ok=True)
        if not existed:
            created.append(path)
    return created


def quote_yaml(value):
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def normalize_task_id(raw_task_id):
    task_id = slugify(raw_task_id)
    if not task_id:
        raise ValueError("task_id must contain at least one letter or digit")
    return task_id


def validate_targets(monitor_type, targets):
    if monitor_type not in VALID_MONITOR_TYPES:
        raise ValueError(f"monitor_type must be one of: {', '.join(sorted(VALID_MONITOR_TYPES))}")

    if monitor_type == "asin" and len(targets) != 1:
        raise ValueError("asin monitor requires exactly one target")
    if monitor_type == "multi-asin" and len(targets) < 2:
        raise ValueError("multi-asin monitor requires at least two targets")
    if monitor_type in {"seller", "brand"} and len(targets) != 1:
        raise ValueError(f"{monitor_type} monitor requires exactly one target")


def render_targets_block(monitor_type, targets):
    if monitor_type == "asin":
        return f"  asin: {quote_yaml(targets[0])}"
    if monitor_type == "multi-asin":
        lines = ["  asins:"]
        lines.extend(f"    - {quote_yaml(target)}" for target in targets)
        return "\n".join(lines)
    key = "seller" if monitor_type == "seller" else "brand"
    return f"  {key}: {quote_yaml(targets[0])}"


def render_list_block(values, indent):
    return "\n".join(f"{indent}- {quote_yaml(value)}" for value in values)


def render_template(template_text, replacements):
    content = template_text
    for key, value in replacements.items():
        content = content.replace(f"__{key}__", value)
    return content


def write_file(path, content, force):
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists; use --force to overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n")


def load_template(name):
    return (Path(__file__).resolve().parent.parent / "assets" / name).read_text()


def build_task_files(args, workspace):
    if not args.task_id:
        return []

    if not args.monitor_type:
        raise ValueError("--monitor-type is required when --task-id is provided")
    if args.mcp not in VALID_MCPS:
        raise ValueError(f"--mcp must be one of: {', '.join(sorted(VALID_MCPS))}")

    targets = split_csv(args.target)
    if not targets:
        raise ValueError("at least one --target is required when --task-id is provided")
    validate_targets(args.monitor_type, targets)

    cadences = split_csv(args.cadence) or list(VALID_CADENCES)
    invalid_cadences = [cadence for cadence in cadences if cadence not in VALID_CADENCES]
    if invalid_cadences:
        raise ValueError(f"invalid cadence(s): {', '.join(invalid_cadences)}")

    focus = split_csv(args.focus) or DEFAULT_FOCUS
    task_id = normalize_task_id(args.task_id)
    daily_doc = args.daily_doc or f"docs/{task_id}-daily.md"
    weekly_doc = args.weekly_doc or f"docs/{task_id}-weekly.md"
    snapshot_dir = args.snapshot_dir or f"snapshots/{task_id}"

    task_template = load_template("task-config.template.yaml")
    daily_template = load_template("daily-report.template.md")
    weekly_template = load_template("weekly-report.template.md")

    replacements = {
        "TASK_ID": task_id,
        "PRIORITY": str(args.priority),
        "MARKETPLACE": args.marketplace,
        "MONITOR_TYPE": args.monitor_type,
        "TARGETS_BLOCK": render_targets_block(args.monitor_type, targets),
        "MCP": args.mcp,
        "CADENCE_BLOCK": render_list_block(cadences, "  "),
        "DAILY_DOC": daily_doc,
        "WEEKLY_DOC": weekly_doc,
        "SNAPSHOT_DIR": snapshot_dir,
        "FOCUS_BLOCK": render_list_block(focus, "  "),
        "NOTES": args.notes or "",
        "TARGETS": ", ".join(targets),
    }

    created = []
    config_path = workspace / "tasks" / f"{task_id}.yaml"
    write_file(config_path, render_template(task_template, replacements), args.force)
    created.append(config_path)

    snapshot_path = workspace / snapshot_dir
    snapshot_path.mkdir(parents=True, exist_ok=True)
    created.append(snapshot_path)

    if "daily" in cadences:
        daily_path = workspace / daily_doc
        write_file(daily_path, render_template(daily_template, replacements), args.force)
        created.append(daily_path)

    if "weekly" in cadences:
        weekly_path = workspace / weekly_doc
        write_file(weekly_path, render_template(weekly_template, replacements), args.force)
        created.append(weekly_path)

    return created


def parse_args():
    parser = argparse.ArgumentParser(
        description="Initialize an Amazon competitor monitoring workspace and optional task.",
    )
    parser.add_argument("--workspace", required=True, help="Workspace path")
    parser.add_argument("--task-id", help="Task identifier; omit to create base folders only")
    parser.add_argument("--monitor-type", choices=sorted(VALID_MONITOR_TYPES))
    parser.add_argument("--target", action="append", default=[], help="Repeat or comma-separate targets")
    parser.add_argument("--mcp", default="sellersprite-mcp", choices=sorted(VALID_MCPS))
    parser.add_argument("--marketplace", default="US")
    parser.add_argument("--cadence", action="append", default=[], help="Repeat or comma-separate cadences")
    parser.add_argument("--priority", type=int, default=50)
    parser.add_argument("--daily-doc")
    parser.add_argument("--weekly-doc")
    parser.add_argument("--snapshot-dir")
    parser.add_argument("--focus", action="append", default=[], help="Repeat or comma-separate focus fields")
    parser.add_argument("--notes", default="")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    workspace = Path(args.workspace).resolve()
    workspace.mkdir(parents=True, exist_ok=True)

    created_dirs = ensure_dirs(workspace)
    created_files = build_task_files(args, workspace)

    if created_dirs:
        print("Created directories:")
        for path in created_dirs:
            print(f"- {path}")
    else:
        print("Workspace directories already existed.")

    if created_files:
        print("Created task artifacts:")
        for path in created_files:
            print(f"- {path}")
    else:
        print("No task files created. Use --task-id to scaffold a task config and report docs.")


if __name__ == "__main__":
    try:
        main()
    except (FileExistsError, ValueError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)
