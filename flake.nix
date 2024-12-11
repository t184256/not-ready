{
  description = "'Not ready' book and accompanying code.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        noto-fonts-extracondensed = pkgs.stdenvNoCC.mkDerivation {
          name = "noto-fonts-extracondensed";
          inherit (pkgs.noto-fonts) version src;
          installPhase = ''
            mkdir -p $out/share/fonts/noto/
            cp -va fonts/NotoSans/unhinted/*/NotoSans-ExtraCondensed* \
                   $out/share/fonts/noto/
            cp -va fonts/NotoSerif/unhinted/*/NotoSerif-ExtraCondensed* \
                   $out/share/fonts/noto/
          '';
        };
        noto-fonts-extracondensed-fontconfig = pkgs.stdenvNoCC.mkDerivation {
          name = "noto-fonts-extracondensed-fontconfig";
          inherit (pkgs.noto-fonts) version;
          nativeBuildInputs = with pkgs; [ fontconfig ];
          phases = [ "installPhase" ];
          installPhase = ''
            mkdir -p $out
            HOME="$out" fc-cache -f -v ${noto-fonts-extracondensed}/share
          '';
        };
        tex = pkgs.texlive.combine {
          inherit (pkgs.texlive)
            scheme-small
            sectsty tocloft csquotes footmisc
            collection-langcyrillic;
        };
        deps = with pkgs; [
          gnumake gnugrep gnused
          pandoc
          ocamlPackages.cpdf
          tex
          noto-fonts-extracondensed noto-fonts-extracondensed-fontconfig
          (python3.withPackages (ps: with ps; [ps.pypdf2 ruamel-yaml]))
          ltex-ls
        ];
        pdf = pkgs.stdenv.mkDerivation rec {
          name = "not-ready-${bookVersion}";
          bookVersion = "1.0.2";  # scraped
          src = ./.;
          nativeBuildInputs = deps;
          phases = [ "unpackPhase" "patchPhase" "buildPhase" ];
          FONTCONFIG_HOME = noto-fonts-extracondensed-fontconfig;
          STRICT = "1";
          enableParallelBuilding = true;
          patchPhase = "patchShebangs maint/*.py";
          makeFlags = [
            "-f" "maint/Makefile" "DESTDIR=${placeholder "out"}" "outputs"
          ];
        };
      in
      {
        devShells.default = pkgs.mkShell {
          nativeBuildInputs = deps;
          FONTCONFIG_HOME = noto-fonts-extracondensed-fontconfig;
        };
        packages.default = pdf;
      }
    );
}
