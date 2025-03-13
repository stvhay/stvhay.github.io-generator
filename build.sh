#!/bin/bash

# handle command line arguments and options
args_opts()
{
    # Process command line arguments
    for arg in "$@"
    do
        case $arg in
            --no-tex)
                tex_enabled=false
                shift
            ;;
            --no-pretty)
                pretty_enabled=false
                shift
            ;;
        esac
    done
}

# clean the generated website directory "public"
clean_public()
{
    git -C public rm -rf --cached .
    git -C public clean -fd
    git -C public checkout main .gitignore
    if ! $tex_enabled 
    then
        git -C public checkout main -- "docs/**/*.pdf"
    fi
}

# format the html and js in the generated website
prettify()
{
    npx prettier public --write
}

# generate .pdf files from LaTeX
build_latex()
{
    local base_dir=$(pwd)
    mkdir -pv latex
    cd "${base_dir}/latex" || return 1
    while IFS= read -r texfile
    do
        echo "Building: $texfile"
        texdir=$(dirname "$texfile")
        filename=$(basename "$texfile")
        
        cd "$texdir" >/dev/null || continue
        
        latexmk -pdf "$filename" >/dev/null
        latexmk -c >/dev/null
        rm -f "${filename%.tex}".{dvi,bbl} ./*.fls
        
        mkdir -p "${base_dir}/static/docs/$texdir"
        mv "${filename%.tex}.pdf" "${base_dir}/static/docs/$texdir/"
        cd - >/dev/null || continue
    done < latex.manifest
    cd "${base_dir}" || return 1
}

# Clean the built .pdf files from the working directory.
clean_latex_pdf() 
{
    while IFS= read -r texfile
    do
        rm -f static/docs/"${texfile%.tex}.pdf" 
    done < latex/latex.manifest
}

## main script

tex_enabled=true
pretty_enabled=true
args_opts "$@"

clean_public

if $tex_enabled
then
    build_latex
fi

hugo
clean_latex_pdf

if $pretty_enabled 
then 
    prettify
fi

git -C public add --all
