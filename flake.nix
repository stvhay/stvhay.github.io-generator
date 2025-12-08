{
  description = "Hugo website build environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            # Hugo static site generator (extended version)
            hugo

            # LaTeX toolchain for PDF generation (minimal setup matching CI)
            (texlive.combine {
              inherit (texlive)
                scheme-basic
                latex-bin
                latexmk

                # Core LaTeX packages (texlive-latex-base, texlive-latex-extra)
                amsmath tools graphics

                # Bibliography support (texlive-bibtex-extra)
                biber biblatex logreq xstring

                # Font packages (texlive-fonts-recommended, texlive-fonts-extra)
                collection-fontsrecommended
                collection-fontsextra

                # Additional packages for CV template
                mdwtools relsize hyperref xcolor url microtype tex-gyre geometry;
            })

            # ExifTool for PDF metadata manipulation
            exiftool

            # Additional build tools
            openssl      # For SHA-384 hashing
            git          # Version control

            # Testing tools
            htmltest     # HTML validation and link checking
            python3      # Python runtime for pytest
            python3Packages.pytest  # Python testing framework

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
            echo "  - htmltest: $(htmltest --version 2>&1)"
            echo "  - pytest: $(pytest --version 2>&1 | head -n1)"
            echo ""
            echo "Run './build' to build the website"
          '';
        };
      }
    );
}
