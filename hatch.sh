#!/bin/bash
set -ex
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

hatch clean
hatch fmt
hatch build --clean
hatch test --all --cover --parallel --randomize