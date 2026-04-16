{
  description = "cad-viewer-widget — development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
    utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, utils }:
    utils.lib.eachSystem [ "x86_64-linux" "aarch64-linux" "aarch64-darwin" ] (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python3;

      in {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            python
            python.pkgs.pip
            python.pkgs.virtualenv
            python.pkgs.conda
            pkgs.nodejs_20
            pkgs.yarn
          ];

          shellHook = ''
            echo "cad-viewer-widget dev environment"
            echo ""
            echo "  Python runtime is provided by Nix; project libraries are not."
            echo ""
            echo "  First-time setup:"
            echo "    python -m venv .venv"
            echo "    source .venv/bin/activate"
            echo "    python -m pip install -U pip"
            echo "    python -m pip install -e ."
            echo "    cd js && yarn install && cd .."
            echo ""
            echo "  Build JS bundle (production):"
            echo "    cd js && yarn build:prod && cd .."
            echo ""
            echo "  Build JS bundle (dev/watch):"
            echo "    cd js && yarn build && cd .."
            echo "    cd js && yarn watch   (in a second terminal)"
            echo ""
          '';
        };
      }
    );
}
