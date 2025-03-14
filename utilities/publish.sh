publish()
(
pushd "$hugo_repo_dir"  || return

    msg_arg=("-m")
    case $# in
        0) : ;;
        1) msg_arg+=("$1") ;;
        *)
            >&2 echo "Usage:"
            >&2 echo "    $0 commit_message"
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
