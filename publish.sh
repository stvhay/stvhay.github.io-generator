#!/bin/bash

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

git -C public add --all
git -C public commit -s "${msg_arg[@]}"
git -C push
