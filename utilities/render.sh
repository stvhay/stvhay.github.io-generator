# shellcheck shell=bash
render()
(
set -eu

    usage()
    {
        cat << EOF
    Usage: render [options] <file.tex>

    Compiles a single LaTeX document and leaves the PDF in its destination
    directory, cleaning up intermediate files.

    Documents under latex/ render to latex/output/<dir>/, which is gitignored
    and mounted to static/docs by Hugo. Documents anywhere else render beside
    their source, so drafts are never staged for the website.

    Unlike ./build, this does not consult latex/latex.manifest, skip unchanged
    documents, or stamp the PDF with its source hash. Use ./build to produce
    PDFs for publication.

    Options:
    -o, --output DIR  Write the PDF to DIR instead of the default destination
    -h, --help        Display this help message and exit

    Arguments:
    file.tex          Path to the LaTeX source
EOF
    }



    # Parse arguments. Paths are resolved against the caller's directory, which
    # must happen before switching to the repository root below.
    tex_file=
    output_dir=
    while [[ $# -gt 0 ]]
    do
        case "$1" in
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

    if ! command -v latexmk >/dev/null 2>&1
    then
        >&2 echo "Error: latexmk not found. Run inside the nix environment:"
        >&2 echo "    nix develop --command ./render $tex_file"
        exit 1
    fi

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



    # Compile from the source directory so relative \addbibresource paths resolve
    cd "$tex_dir" || exit 1
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

    mkdir -p "$output_dir"
    if [[ "$output_dir" != "$tex_dir" ]]
    then
        mv "${base_name}.pdf" "${output_dir}/"
    fi
    echo "Rendered: ${output_dir}/${base_name}.pdf"
)
