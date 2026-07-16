# shellcheck shell=bash
#
# Helpers shared by build and render for producing LaTeX document artifacts.
#
# Every artifact is stamped with the SHA-384 hash of its .tex source so the
# build can detect whether the source changed since the artifact was last
# generated: PDFs carry it in XMP metadata, HTML in a <meta> tag.

getlatexhash() { openssl dgst -sha384 -r "$1" | cut -d ' ' -f 1; }

getpdfhash()   { exiftool -XMP-pdfx:texhash -b "$1"; }

# Tolerates prettier's reformatting (attributes split across lines).
gethtmlhash()
{
    tr -d '\n' < "$1" 2>/dev/null \
        | sed -n 's/.*name="texhash"[[:space:]]*content="\([0-9a-f]*\)".*/\1/p'
}

markpdf()
{
    local tex_file="$1"
    local pdf_file="${2:-${tex_file%.tex}.pdf}"
    local config
    config=$(mktemp) || return 1

    # configure exiftool to create the custom metadata
    {
        printf "%s\n" "%Image::ExifTool::UserDefined = ("
        printf "%s\n" "    'Image::ExifTool::XMP::pdfx' => {"
        printf "%s\n" "        texhash => { Writable => 'string' },"
        printf "%s\n" "    },"
        printf "%s\n" "); 1;"
    } > "$config"

    local hash
    hash=$(getlatexhash "$tex_file") || return 1
    if ! exiftool -config "$config" \
        -XMP-pdfx:texhash="$hash" \
        "$pdf_file" >/dev/null
    then
        return 1
    fi
    rm -f "${pdf_file}_original"
    rm -f "$config"
}

# Converts a .tex file to HTML with latexmlc and finishes the <head>:
# LaTeXML is invoked with --nodefaultresources so nothing is copied next to
# the document; instead the site-wide stylesheet copies under
# static/css/latexml/ are linked, along with the favicon (required in every
# static HTML file) and the texhash stamp.
renderhtml()
{
    local tex_file="$1"
    local html_file="$2"

    local latexml_log
    latexml_log=$(mktemp) || return 1
    if ! latexmlc --nodefaultresources \
        --log="$latexml_log" \
        --dest="$html_file" \
        "$tex_file" >/dev/null 2>&1
    then
        >&2 echo "Error converting $tex_file to HTML"
        >&2 cat "$latexml_log"
        rm -f "$latexml_log"
        return 1
    fi
    # latexmlc exits 0 on recoverable conversion errors; surface them
    # without failing the build.
    grep '^Error:' "$latexml_log" >&2 || true
    rm -f "$latexml_log"

    local hash
    hash=$(getlatexhash "$tex_file") || return 1
    python3 - "$html_file" "$hash" <<'PYEOF'
import sys

path, texhash = sys.argv[1], sys.argv[2]
head = (
    '<link rel="icon" href="/favicon.ico" sizes="32x32">'
    '<link rel="icon" href="/favicon.svg" type="image/svg+xml">'
    '<link rel="stylesheet" href="/css/latexml/LaTeXML.css" type="text/css">'
    '<link rel="stylesheet" href="/css/latexml/ltx-article.css" type="text/css">'
    '<link rel="stylesheet" href="/css/latexml/site.css" type="text/css">'
    f'<meta name="texhash" content="{texhash}">'
)
html = open(path, encoding="utf-8").read()
if "</head>" not in html:
    sys.exit(f"no </head> in {path}")
# LaTeXML declares the encoding with the legacy http-equiv form; swap it
# for the HTML5 charset meta the site standard expects.
html = html.replace(
    '<meta http-equiv="content-type" content="text/html; charset=UTF-8">',
    '<meta charset="utf-8">',
    1,
)
open(path, "w", encoding="utf-8").write(html.replace("</head>", head + "</head>", 1))
PYEOF
}
