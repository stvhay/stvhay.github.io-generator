{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    # Hugo static site generator (extended version)
    hugo

    # LaTeX toolchain for PDF generation
    texlive.combined.scheme-full

    # ExifTool for PDF metadata manipulation
    exiftool

    # Additional build tools
    openssl      # For SHA-384 hashing
    git          # Version control

    # Node.js tools (for prettier formatting)
    nodejs
    nodePackages.prettier
  ];

  shellHook = ''
    echo "Hugo website build environment loaded"
    echo "Available tools:"
    echo "  - hugo: $(hugo version 2>&1 | head -n1)"
    echo "  - exiftool: $(exiftool -ver)"
    echo "  - latexmk: $(latexmk -v 2>&1 | head -n1)"
    echo ""
    echo "Run './build' to build the website"
  '';
}
