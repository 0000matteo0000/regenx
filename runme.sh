#!/bin/bash
set -ex
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

export PIP_BREAK_SYSTEM_PACKAGES=1
# python3 -m pytest --cov="./src/regenx" --showlocals --show-capture="all" --full-trace --quiet "."
python3 -m build