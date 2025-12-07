# shellcheck shell=bash
publish()
(
set -eu
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

    # Check if there are changes to commit in public/
    if git -C public diff-index --quiet HEAD -- 2>/dev/null; then
        echo "No changes to publish in public/"
    else
        git -C public commit -s "${msg_arg[@]}" || {
            >&2 echo "Failed to commit changes in public/"
            exit 1
        }
        git -C public push || {
            >&2 echo "Failed to push changes in public/"
            exit 1
        }
    fi

    # Check if there are changes to commit in source repo
    if git diff-index --quiet HEAD -- 2>/dev/null; then
        echo "No changes to commit in source repo"
    else
        git add --all
        git commit -s "${msg_arg[@]}" || {
            >&2 echo "Failed to commit changes in source repo"
            exit 1
        }
        git push || {
            >&2 echo "Failed to push changes in source repo"
            exit 1
        }
    fi

popd || return
)
