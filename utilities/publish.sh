# shellcheck shell=bash
publish()
( 
pushd "${hugo_repo_dir:?}"  || return

    case $#
    in
        0) : ;;
        1)
            msg_arg=("-m" "$1")
            ;;
        *)
            >&2 echo "Usage:"
            >&2 echo "    $0 [commit_message]"
            exit 1
            ;;
    esac

    git -C public commit -s "${msg_arg[@]}"
    git -C public push
    git add --all
    git commit -s "${msg_arg[@]}"
    git push

popd || return
)
