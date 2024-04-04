#!/usr/bin/env bash

set -eu

project_root="$(cd "$(dirname "$(dirname "$0")")" && pwd)"
imgs="${project_root}/.img"
license="${imgs}/license.svg"
python="${imgs}/python.svg"
pypi="${imgs}/pypi.svg"

get_version () {
  cat "${project_root}/ocui/res/VERSION"
}

python -m pybadges \
    --left-text="python" \
    --right-text="3.10, 3.11" \
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
