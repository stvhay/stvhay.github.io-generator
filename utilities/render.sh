# shellcheck shell=bash
render()
(
set -eu

    usage()
    {
        cat << EOF
    Usage: render [options] <file.tex>

    Compiles a single LaTeX document and leaves the output in its destination
    directory, cleaning up intermediate files.

    Documents under latex/ render to latex/output/<dir>/, which is gitignored
    and mounted to static/docs by Hugo. Documents anywhere else render beside
    their source, so drafts are never staged for the website.

    HTML output links the site-served stylesheets (/css/latexml/) and favicon,
    so it displays fully styled only when served by the site (e.g. through
    'hugo server'), not when opened directly from disk.

    Unlike ./build, this does not consult latex/latex.manifest, skip unchanged
    documents, or stamp the PDF with its source hash. Use ./build to produce
    documents for publication.

    Options:
    -f, --format FMT  Output format: pdf (default), html, or both
    -o, --output DIR  Write the output to DIR instead of the default destination
    -h, --help        Display this help message and exit

    Arguments:
    file.tex          Path to the LaTeX source
EOF
    }



    # Parse arguments. Paths are resolved against the caller's directory, which
    # must happen before switching to the repository root below.
    tex_file=
    output_dir=
    format=pdf
    while [[ $# -gt 0 ]]
    do
        case "$1" in
            -f|--format)
                case "${2:-}" in
                    pdf|html|both)
                        format="$2"
                        shift 2
                    ;;
                    *)
                        >&2 echo "Error: --format must be pdf, html, or both"
                        >&2 usage
                        exit 1
                    ;;
                esac
            ;;
            -o|--output)
                if [[ -n "${2:-}" && "$2" != -* ]]
                then
                    output_dir="$2"
                    shift 2
                else
                    >&2 echo "Error: --output requires a value"
                    >&2 usage
                    exit 1
                fi
            ;;
            -h|--help)
                usage
                exit
            ;;
            --*|-*)
                >&2 echo "Unknown option: $1"
                >&2 usage
                exit 1
            ;;
            *)
                if [[ -n "$tex_file" ]]
                then
                    >&2 echo "Error: only one .tex file may be given"
                    >&2 usage
                    exit 1
                fi
                tex_file="$1"
                shift
            ;;
        esac
    done

    if [[ -z "$tex_file" ]]
    then
        usage
        exit 1
    fi

    if [[ "$tex_file" != *.tex ]]
    then
        >&2 echo "Error: not a LaTeX source file: $tex_file"
        exit 1
    fi

    if [[ ! -f "$tex_file" ]]
    then
        >&2 echo "Error: no such file: $tex_file"
        exit 1
    fi

    for tool in latexmk latexmlc
    do
        if ! command -v "$tool" >/dev/null 2>&1
        then
            >&2 echo "Error: $tool not found. Run inside the nix environment:"
            >&2 echo "    nix develop --command ./render $tex_file"
            exit 1
        fi
    done

    tex_dir=$(cd "$(dirname "$tex_file")" && pwd)
    tex_name=$(basename "$tex_file")
    base_name="${tex_name%.tex}"
    if [[ -n "$output_dir" ]]
    then
        mkdir -p "$output_dir"
        output_dir=$(cd "$output_dir" && pwd)
    fi

    pushd "${hugo_repo_dir:?}" >/dev/null || return
    repo_root=$(pwd)
    popd >/dev/null || return

    # Documents under latex/ follow the build script's layout so their PDFs land
    # where Hugo expects them; everything else stays put.
    if [[ -z "$output_dir" ]]
    then
        case "$tex_dir/" in
            "$repo_root"/latex/*)
                relative_dir="${tex_dir#"$repo_root"/latex/}"
                output_dir="${repo_root}/latex/output/${relative_dir}"
            ;;
            *)
                output_dir="$tex_dir"
            ;;
        esac
    fi



    # Compile from the source directory so relative \bibliography paths resolve
    cd "$tex_dir" || exit 1
    mkdir -p "$output_dir"

    if [[ "$format" == pdf || "$format" == both ]]
    then
        latex_log=$(mktemp) || exit 1
        if ! latexmk -quiet -pdf "$tex_name" >"$latex_log" 2>&1
        then
            >&2 echo "Error compiling $tex_file"
            >&2 cat "$latex_log"
            rm -f "$latex_log"
            exit 1
        fi
        rm -f "$latex_log"

        latexmk -c >/dev/null 2>&1
        rm -f "${base_name}".{dvi,bbl,fls,run.xml}

        if [[ "$output_dir" != "$tex_dir" ]]
        then
            mv "${base_name}.pdf" "${output_dir}/"
        fi
        echo "Rendered: ${output_dir}/${base_name}.pdf"
    fi

    if [[ "$format" == html || "$format" == both ]]
    then
        renderhtml "$tex_name" "${output_dir}/${base_name}.html" || exit 1
        echo "Rendered: ${output_dir}/${base_name}.html"
    fi
)
