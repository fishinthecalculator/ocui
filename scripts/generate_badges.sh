#!/usr/bin/env bash

set -eu

project_root="$(cd "$(dirname "$(dirname "$0")")" && pwd)"
init_py="${project_root}/ocui/__init__.py"
imgs="${project_root}/.img"
license="${imgs}/license.svg"
python="${imgs}/python.svg"
pypi="${imgs}/pypi.svg"

get_version () {
  cat "$init_py" | grep version | sed -E 's/^.*__version__ = "(.*)".*$/\1/'
}

python -m pybadges \
    --left-text="python" \
    --right-text="3.10, 3.11, 3.12" \
    --whole-link="https://www.python.org/" \
    --logo='https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/python.svg' \
    --embed-logo=yes > "${python}"

python -m pybadges \
    --left-text="pypi" \
    --right-text="$(get_version)" \
    --whole-link="https://pypi.org/project/ocui/" > "${pypi}"

python -m pybadges \
    --left-text="LICENSE" \
    --right-text="GPL 3.0+" \
    --whole-link="https://choosealicense.com/licenses/gpl-3.0/" > "${license}"
