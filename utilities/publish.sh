# shellcheck shell=bash
publish()
( 
pushd "${hugo_repo_dir:?}"  || return

    msg_arg=("-m")
    if [[ $# -ne 1 ]]
    then
        >&2 echo "Usage:"
        >&2 echo "    $0 commit_message"
        exit 1
    fi
    msg_arg+=("$1")
    git -C public commit -s "${msg_arg[@]}"
    git -C public push
    git add --all
    git commit -s "${msg_arg[@]}"
    git push

popd || return
)
