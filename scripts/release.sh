#!/usr/bin/env bash

set -eu

myself="$(basename "$0")"
init_py="$(pwd)/ocui/__init__.py"
channel_scm="$(pwd)/.guix/modules/ocui.scm"
generate_badges="$(pwd)/scripts/generate_badges.sh"
imgs="$(pwd)/.img"

current_branch="$(git rev-parse --abbrev-ref HEAD)"
current_commit="$(git log -1 --format='%H')"
dryrun=0
verbose=0
publish=0
bump="INVALID"

required_commands=("getopt" "pysemver" "git" "flit")
valid_types=('major' 'minor' 'patch' 'prerelease' 'build')

error() {
  echo -e "$@" >/dev/fd/2
}

crash() {
  [ "$#" -gt 0 ] && error "$1"
  exit 1
}

check-dependencies() {
  for com in "${required_commands[@]}"; do
    if ! command -v "$com" >/dev/null; then
      error "$com not found but it's required! Please install it with your favourite package manager."
      crash "\n\t\t\t\tOr just use Guix ;)\n"
    fi
  done
}

usage() {
  cat <<EOF
Usage: ${myself} -b <bump-type> [-hpbvd]
Release a new version of ocui according to https://semver.org

-h,          --help                  Show this help message.

-b,          --bump                  Select a version bump type

-p,          --publish               Publish current release to PyPI.

-d,          --dryrun                Show operations, instead of carrying them out.

             --list-types            List all valid version bump types.

-v,          --verbose               Run script in verbose mode. Will print out each step of execution.
EOF
}

validate-bump-type() {
  if [[ ${valid_types[*]} =~ (^|[[:space:]])"$1"($|[[:space:]]) ]]; then
    true
  else
    crash "Invalid bump type: $1"
  fi
}

current-version() {
  cat "$init_py" | grep version | sed -E 's/^.*__version__ = "(.*)".*$/\1/'
}

release-new-version() {
  current="$(current-version)"
  next="$(pysemver bump "$1" "$current")"
  echo "RELEASING VERSION: ${next}"

  [ "$verbose" = "1" ] && echo "Updating ${init_py}..."
  [ "$dryrun" = "0" ] && sed -i -E "s/__version__.*=.*\"${current}\"$/__version__ = \"${next}\"/" "$init_py"

  [ "$verbose" = "1" ] && echo "Updating ${channel_scm}..."
  [ "$dryrun" = "0" ] && sed -i "s/${current}/${next}/g" "$channel_scm"

  if command -v "guix" >/dev/null; then

    [ "$verbose" = "1" ] && echo "Generating badges..."
    [ "$dryrun" = "0" ] && guix shell python-wrapper python-pybadges -- "${generate_badges}" && git add "${imgs}"

  fi

  [ "$verbose" = "1" ] && echo "Committing ${init_py} and ${channel_scm}"
  [ "$dryrun" = "0" ] && git add "${init_py}"  \
                                 "${channel_scm}"  && \
                         git commit -m "Release v${next}."

  [ "$verbose" = "1" ] && echo "Tagging Git HEAD with v${next}"
  [ "$dryrun" = "0" ] && git tag "v${next}"

  [ "$verbose" = "1" ] && echo "Building package..."
  [ "$dryrun" = "0" ] && flit build

}

restore-git-state () {
  # This way we can go back to a
  # detached HEAD state as well.
  if [ "${current_branch}" = "HEAD" ]; then
    git checkout "${current_commit}"
  else
    git checkout "${current_branch}"
  fi
}

parse-args() {
  [ "$#" -eq 0 ] && crash "$(usage)"

  options=$(getopt -l "help,publish,bump:,list-types,verbose,dryrun" -o "hpb:vd" -- "$@")

  # set --:
  # If no arguments follow this option, then the positional parameters are unset. Otherwise, the positional parameters
  # are set to the arguments, even if some of them begin with a ‘-’.
  eval set -- "$options"

  while true; do
    case $1 in
    -h | --help)
      usage
      exit 0
      ;;
    --list-types)
      echo "${valid_types[@]}"
      exit 0
      ;;
    -v | --verbose)
      verbose=1
      set -vx
      ;;
    -d | --dryrun)
      dryrun=1
      verbose=1
      ;;
    -p | --publish)
      publish=1
      ;;
    -b | --bump)
      shift
      bump="$1"
      ;;
    --)
      shift
      break
      ;;
    esac
    shift
  done

  if [ "$bump" = "INVALID" ] && [ "$publish" = "0" ]; then
    error "You can either build a new release or publish the current release to PyPI."
    crash "See ${myself} -h for more information."
  fi
}

parse-args "$@"

if [ "$bump" != "INVALID" ]; then
    check-dependencies
    validate-bump-type "$bump"
    release-new-version "$bump"
fi

if [ "$publish" = "1" ]; then

  # We make sure to actually publish the tagged version
  git checkout "v$(current-version)"
  set +e
  # If this command fails we still want to go back to the
  # branch we were on.
  FLIT_USERNAME="__token__"
  SOURCE_DATE_EPOCH=$(date +%s)
  flit publish
  set -e
  restore-git-state
fi

exit 0
