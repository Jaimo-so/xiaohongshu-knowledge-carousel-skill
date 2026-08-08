#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/skill/create-xiaohongshu-knowledge-carousel"
TARGET_ROOT="${CODEX_HOME:-$HOME/.codex}/skills"

if [[ "${1:-}" == "--target-root" ]]; then
  if [[ -z "${2:-}" ]]; then
    echo "--target-root requires a directory" >&2
    exit 1
  fi
  TARGET_ROOT="$2"
elif [[ $# -gt 0 ]]; then
  echo "Usage: bash install.sh [--target-root DIRECTORY]" >&2
  exit 1
fi

TARGET_DIR="$TARGET_ROOT/create-xiaohongshu-knowledge-carousel"

if [[ ! -f "$SOURCE_DIR/SKILL.md" ]]; then
  echo "Skill source not found: $SOURCE_DIR" >&2
  exit 1
fi

mkdir -p "$TARGET_ROOT"

if [[ -e "$TARGET_DIR" ]]; then
  echo "Target already exists: $TARGET_DIR" >&2
  echo "Remove or rename it before reinstalling." >&2
  exit 1
fi

cp -R "$SOURCE_DIR" "$TARGET_DIR"
echo "Installed to: $TARGET_DIR"
echo "Restart Codex or begin a new task to load the Skill."
