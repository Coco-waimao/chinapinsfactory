#!/bin/sh
# Install the local check as a git hook so it runs before every commit and
# every push. Safe to run more than once.

set -e

ROOT="$(git rev-parse --show-toplevel)"
HOOKS="$(git rev-parse --git-path hooks)"
mkdir -p "$HOOKS"

for name in pre-commit pre-push; do
    cp "$ROOT/scripts/hook-local-check.sh" "$HOOKS/$name"
    chmod +x "$HOOKS/$name" 2>/dev/null || true
    echo "installed $HOOKS/$name"
done

echo
echo "The local check now runs automatically before each commit and push."
echo "Run it manually at any time with: python scripts/check.py"
