{ stdenv, lib, poetry2nix, ... }:

let
  vnumber = "1.0.0";
  manifest = (lib.importTOML ./pyproject.toml).tool.poetry;
in
poetry2nix.mkPoetryApplication rec {

  pname = manifest.name;
  version = "${vnumber}-beta";

  projectDir = ./.;

  meta = with lib; {
    description = manifest.description;
    homepage = "https://github.com/gp2112/querolerbot";
    license = licenses.agpl3;
    maintainers = [ maintainers.gp2112 ];
    platforms = platforms.all;
  };

}
