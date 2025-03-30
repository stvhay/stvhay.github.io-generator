# shellcheck shell=bash
post()
( 
pushd "${hugo_repo_dir:?}"  || return

    usage()
    {
        cat << EOF
    Usage: $(basename "$0") [options] [title]

    Options:
    --page PAGE      Specify page (Default: writing)
    -h, --help       Display this help message and exit

    Arguments:
    title            Post title
EOF
    }



    # Parse arguments
    page_group=writing
    single_md=false
    convert=false
    while [[ $# -gt 0 ]]
    do
        case "$1" in
            --page)
                if [[ -n "$2" && "$2" != -* ]]
                then
                    page_group="$2"
                    shift 2
                else
                    >&2 echo "Error: --option requires a value"
                    >&2 usage
                fi
            ;;
            --single)
                single_md=true
                shift
            ;;
            --convert)
                convert=true
                shift
            ;;
            -h|--help)
                usage
                exit
            ;;
            --*|-*)
                echo "Unknown option: $1" >&2
                usage
                exit 1
            ;;
            *)
                # Save positional arguments
                args+=("$1")
                shift
            ;;
        esac
    done
    set -- "${args[@]}"
    if [[ ! $# -eq 1 ]]
    then
        usage
        exit 1
    else
        title="$1"
    fi



    # Make the post
    post_path="content/${page_group}/${title}"
    if $single_md
    then
        if [[ ! -f "${post_path}.md" ]]
        then
            if [[ ! -d "${post_path}" ]]
            then
                hugo new content "${post_path}.md"
            else
                >&2 echo "Already exists: ${post_path}"
                >&2 echo "Convert manually."
                exit 1
            fi
        fi
        target="${post_path}.md"
    else
        if [[ ! -d "${post_path}" ]]
        then
            if [[ ! -f "${post_path}.md" ]]
            then
                hugo new content "${post_path}.md"
            else
                if ! $convert
                then 
                    >&2 echo "Already exists: ${post_path}.md"
                    exit 1
                fi
            fi
            mkdir "${post_path}"
            mv "${post_path}.md" "${post_path}/index.md"
        fi
        target="${post_path}/index.md"
    fi
    ${EDITOR:-vi} "$target"
popd || return
)
