#!/usr/bin/env bash

publish_repo=git@github.com:stvhay/stvhay.github.io.git



# Process command line arguments
pretty_enabled=true
git_commit=HEAD   # unless its CI, look at the HEAD for changes
for arg in "$@"
do
    case $arg in
        --no-pretty)
            pretty_enabled=false
            shift
        ;;
        --ci)
            git_commit=HEAD~1
    esac
done



# initialize generated website directory "public"
if [[ ! -d public ]]
then
    git clone "$publish_repo" public
fi

if [[ -d public/.git ]] # website directory is a git repository
then
    git -C public rm -rf --cached .
    git -C public clean -fd
    git -C public checkout main .gitignore
    git -C public checkout main -- "docs/**/*.pdf"
else
    rm -rf public/*
fi



# Build LaTeX documents
modified_files()
{
    { 
        git ls-files --modified --others --exclude-standard
        git diff --cached --name-only
        git diff $git_commit --name-only
    } | grep '\.tex' | sort | uniq
}
base_dir=$(pwd)
mkdir -pv latex
cd "${base_dir}/latex" || exit 1
changed_tex_files=()
while IFS= read -r line; do
    changed_tex_files+=("$line")
done < <(modified_files)
while IFS= read -r texfile
do
    if [[ $(printf " %q " "${changed_tex_files[@]}") =~ $(printf " %q " "$texfile") ]]
    then
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
    fi
done < latex.manifest
cd "${base_dir}" || exit 1



# Build website
hugo
[[ $pretty_enabled ]] && npx prettier public --write --ignore-path=.prettierignore



# Clean any built .pdf files from the working directory.
while IFS= read -r texfile
do
    rm -f static/docs/"${texfile%.tex}.pdf" 
done < latex/latex.manifest



# Stage changes
[[ -d public/.git  ]] && git -C public add --all
git -C public status
