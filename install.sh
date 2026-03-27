#!/usr/bin/env bash

set -eu

REPO="restart2000/amazon-competitor-monitor"
REF="main"
SKILL_NAME="amazon-competitor-monitor"
TARGET="auto"
DEST_ROOT=""

usage() {
  cat <<'EOF'
Usage:
  install.sh [--target codex|openclaw|auto] [--dest DIR] [--ref REF] [--repo OWNER/REPO]

Examples:
  install.sh --target codex
  install.sh --target openclaw
  install.sh --dest "$HOME/.openclaw/skills"
  install.sh --dest "$(pwd)/skills"

Options:
  --target   Install target. auto|codex|openclaw. Default: auto
  --dest     Override the skills root directory. The script installs into DIR/amazon-competitor-monitor
  --ref      Branch or tag to install. Default: main
  --repo     GitHub repo in OWNER/REPO form. Default: restart2000/amazon-competitor-monitor
  -h, --help Show this help
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --target)
      TARGET="$2"
      shift 2
      ;;
    --dest)
      DEST_ROOT="$2"
      shift 2
      ;;
    --ref)
      REF="$2"
      shift 2
      ;;
    --repo)
      REPO="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [ -z "$DEST_ROOT" ]; then
  case "$TARGET" in
    codex)
      DEST_ROOT="${CODEX_HOME:-$HOME/.codex}/skills"
      ;;
    openclaw)
      DEST_ROOT="${OPENCLAW_HOME:-$HOME/.openclaw}/skills"
      ;;
    auto)
      if [ -d "${CODEX_HOME:-$HOME/.codex}/skills" ]; then
        DEST_ROOT="${CODEX_HOME:-$HOME/.codex}/skills"
      elif [ -d "${OPENCLAW_HOME:-$HOME/.openclaw}/skills" ]; then
        DEST_ROOT="${OPENCLAW_HOME:-$HOME/.openclaw}/skills"
      else
        DEST_ROOT="${CODEX_HOME:-$HOME/.codex}/skills"
      fi
      ;;
    *)
      echo "Unsupported --target value: $TARGET" >&2
      exit 1
      ;;
  esac
fi

INSTALL_DIR="${DEST_ROOT%/}/$SKILL_NAME"
TMP_DIR="$(mktemp -d)"
ARCHIVE_PATH="$TMP_DIR/archive.tar.gz"
EXTRACT_DIR="$TMP_DIR/extracted"
mkdir -p "$EXTRACT_DIR"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

download_archive() {
  branch_url="https://github.com/$REPO/archive/refs/heads/$REF.tar.gz"
  tag_url="https://github.com/$REPO/archive/refs/tags/$REF.tar.gz"

  if command -v curl >/dev/null 2>&1; then
    if curl -fsL "$branch_url" -o "$ARCHIVE_PATH"; then
      return 0
    fi
    curl -fsL "$tag_url" -o "$ARCHIVE_PATH"
    return 0
  fi

  if command -v wget >/dev/null 2>&1; then
    if wget -qO "$ARCHIVE_PATH" "$branch_url"; then
      return 0
    fi
    wget -qO "$ARCHIVE_PATH" "$tag_url"
    return 0
  fi

  echo "Neither curl nor wget is available. Please install one of them first." >&2
  exit 1
}

download_archive

tar -xzf "$ARCHIVE_PATH" -C "$EXTRACT_DIR"

SOURCE_DIR="$(find "$EXTRACT_DIR" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
if [ -z "$SOURCE_DIR" ]; then
  echo "Failed to extract repository archive." >&2
  exit 1
fi

mkdir -p "$DEST_ROOT"

if command -v rsync >/dev/null 2>&1; then
  mkdir -p "$INSTALL_DIR"
  rsync -a --delete --exclude '.git' --exclude '.DS_Store' "$SOURCE_DIR/" "$INSTALL_DIR/"
else
  rm -rf "$INSTALL_DIR"
  mkdir -p "$INSTALL_DIR"
  cp -R "$SOURCE_DIR"/. "$INSTALL_DIR"/
  rm -rf "$INSTALL_DIR/.git"
  rm -f "$INSTALL_DIR/.DS_Store"
fi

echo "Installed $SKILL_NAME to: $INSTALL_DIR"
echo "If your app caches skills, restart it to pick up the latest version."
