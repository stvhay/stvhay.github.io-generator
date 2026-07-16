# shellcheck shell=bash

# Absolute, so scripts resolve repo paths after changing directory.
export hugo_repo_dir; hugo_repo_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
for util in "${hugo_repo_dir}"/utilities/*.sh
do
    # shellcheck disable=SC1090
    source "$util"
done
