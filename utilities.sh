# shellcheck shell=bash

export hugo_repo_dir; hugo_repo_dir=$(dirname "${BASH_SOURCE[0]}")
for util in utilities/*.sh
do
    # shellcheck disable=SC1090
    source "$util"
done
