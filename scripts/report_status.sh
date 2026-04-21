#!/usr/bin/env bash
set -euo pipefail
find outputs -maxdepth 3 -type f | sort
find docs/progress -maxdepth 2 -type f | sort
