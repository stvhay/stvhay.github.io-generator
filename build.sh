#!/bin/bash

args()
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

clean()
{
    rm -rf public/*
}

prettify()
{
    npx prettier public --write
}

build_latex()
{
    local pwd=$(pwd)
    mkdir -pv latex
    cd "${pwd}/latex" || return 1
    while IFS= read -r texfile
    do
        echo "Building: $texfile"
        texdir=$(dirname "$texfile")
        filename=$(basename "$texfile")
        
        cd "$texdir" >/dev/null || continue
        
        latexmk -pdf "$filename" >/dev/null
        latexmk -c >/dev/null
        rm -f "${filename}".{dvi,bbl} ./*.fls
        
        mkdir -p "${pwd}/static/docs/$texdir"
        mv "${filename%.tex}.pdf" "${pwd}/static/docs/$texdir/"
        cd - >/dev/null || continue
    done < latex.manifest
    cd "${pwd}" || return 1
}

tex_enabled=true
pretty_enabled=true
args "$@"

clean
$tex_enabled && \
    build_latex
hugo
$pretty_enabled && \
    prettify
