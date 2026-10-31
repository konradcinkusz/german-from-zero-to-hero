#!/usr/bin/env bash
# One command: installs the pre-commit hook.
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
ln -sf "../../scripts/hooks/pre-commit" "$ROOT/.git/hooks/pre-commit"
echo "pre-commit hook installed."
