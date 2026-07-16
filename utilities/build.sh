# shellcheck shell=bash
build()
(
set -eu
pushd "${hugo_repo_dir:?}" || return

    publish_repo=git@github.com:stvhay/stvhay.github.io.git

    # Artifact hashing and generation helpers live in utilities/latex.sh.
    # Manifest lines are "<doc.tex> [formats]" where formats is any of
    # "pdf" and "html"; a line with no formats builds pdf only.



    # Process command line arguments
    pretty_enabled=true
    while [[ $# -gt 0 ]]
    do
        case $1 in
            --no-pretty)
                pretty_enabled=false
                shift
            ;;
            *)
                shift
            ;;
        esac
    done



    # initialize generated website directory "public"
    if [[ ! -d public ]]
    then
        echo "Cloning repository..."
        git clone "$publish_repo" public
    else
        echo "Resetting and pulling repository..."
        git -C public reset --hard HEAD >/dev/null
        git -C public pull >/dev/null
    fi

    if [[ -d public/.git ]] # website directory is a git repository
    then
        # - .gitignore is not created by Hugo
        # - pdf files need special treatment because they change hash each build
        echo "Cleaning and preparing repository..."
        git -C public rm -rf --cached . >/dev/null
        git -C public clean -fd >/dev/null
        git -C public checkout main .gitignore 2>/dev/null

        # read from the manifest; restore only the formats still requested
        # so a format dropped from the manifest disappears from the site
        while read -r tex_file formats
        do
            [[ -z "$tex_file" || "$tex_file" == \#* ]] && continue
            for format in ${formats:-pdf}
            do
                # tolerate artifacts not yet published (new docs or formats)
                git -C public checkout main \
                    "docs/${tex_file%.tex}.${format}" 2>/dev/null || true
            done
        done < latex/latex.manifest
    else
        rm -rf public/*
    fi



    # Build LaTeX documents
    echo "Building LaTeX documents..."
    base_dir=$(pwd)
    mkdir -p latex
    cd "${base_dir}/latex" || exit 1

    # read from the manifest and build what has changed, per format
    while read -r texfile formats
    do
        [[ -z "$texfile" || "$texfile" == \#* ]] && continue
        current_hash=$(getlatexhash "$texfile")
        texdir=${texfile%/*}
        filename=${texfile##*/}
        outdir="${base_dir}/latex/output/$texdir"

        for format in ${formats:-pdf}
        do
            case $format in
                pdf)  previous_hash=$(getpdfhash "${base_dir}/public/docs/${texfile%.tex}.pdf") ;;
                html) previous_hash=$(gethtmlhash "${base_dir}/public/docs/${texfile%.tex}.html") ;;
                *)
                    >&2 echo "Unknown format '$format' for $texfile in latex.manifest"
                    exit 1
                ;;
            esac
            if [[ $current_hash == "$previous_hash" ]]
            then
                echo "Skipping: $texfile ($format unchanged)"
                continue
            fi

            echo "Building: $texfile ($format)"
            mkdir -p "$outdir"
            prev_dir=$PWD
            cd "$texdir" || continue

            case $format in
                pdf)
                    # Compile PDF, save output to temp log for error reporting
                    latex_log=$(mktemp)
                    if ! latexmk -quiet -pdf "$filename" >"$latex_log" 2>&1; then
                        >&2 echo "Error compiling $texfile"
                        >&2 cat "$latex_log"
                        rm -f "$latex_log"
                        cd "$prev_dir" || exit 1
                        exit 1
                    fi
                    rm -f "$latex_log"

                    latexmk -c >/dev/null 2>&1
                    rm -f "${filename%.tex}".{dvi,bbl} ./*.fls

                    markpdf "$filename"
                    mv "${filename%.tex}.pdf" "$outdir/"
                ;;
                html)
                    if ! renderhtml "$filename" "$outdir/${filename%.tex}.html"
                    then
                        cd "$prev_dir" || exit 1
                        exit 1
                    fi
                ;;
            esac
            cd "$prev_dir" || continue
        done
    done < latex.manifest
    cd "${base_dir}" || exit 1



    # Build website
    echo "Building website..."
    hugo || exit 1
    if [[ $pretty_enabled == true ]]
    then
        echo "Formatting content..."
        prettier public --write --ignore-path=.prettierignore || exit 1
    fi



    # Clean any built artifacts from the working directory.
    # These files are used by Hugo (via the latex/output → static/docs mount
    # in hugo.toml) but are not checked into git, as they are regenerated
    # from .tex sources on each build.
    while read -r texfile _
    do
        [[ -z "$texfile" || "$texfile" == \#* ]] && continue
        rm -f "latex/output/${texfile%.tex}".{pdf,html}
    done < latex/latex.manifest



    # Stage changes; show status
    echo '+-----------------------+'
    echo '| Hugo                  |'
    echo '+-----------------------+'
    git status
    if [[ -d public/.git ]]
    then
        git -C public add --all >/dev/null
        echo '+-----------------------+'
        echo '| Website               |'
        echo '+-----------------------+'
        git -C public status
    fi

popd || return
)
