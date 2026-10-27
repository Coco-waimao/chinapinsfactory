#!/bin/sh
# Git hook that runs the local check before a commit or a push.
# Installed by scripts/install-hooks.sh
#
# The check is fast (a couple of seconds) and catches the failures that
# otherwise only show up after the site is live: broken internal links,
# missing images, structured data that does not match the visible page,
# a page that cannot be reached, or a line ending flip.

set -e

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

if command -v python3 >/dev/null 2>&1; then
    PY=python3
elif command -v python >/dev/null 2>&1; then
    PY=python
else
    echo "hook: python not found, skipping local check"
    exit 0
fi

if ! "$PY" scripts/check.py --quiet; then
    echo
    echo "hook: local check failed, the commit/push was not completed."
    echo "      Run 'python scripts/check.py' for the full report."
    exit 1
fi
