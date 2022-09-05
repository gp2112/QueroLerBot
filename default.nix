{ lib, python3Packages, ... }:

let
  vnumber = "1.0.0";
  manifest = (lib.importTOML ./pyproject.toml).project;
in
python3Packages.buildPythonPackage rec {

  pname = manifest.name;
  version = "${vnumber}-beta";

  format = "pyproject";

  src = ./.;

  meta = with lib; with manifest; {
    inherit description;
    homepage = "https://github.com/gp2112/querolerbot";
    license = licenses.agpl3;
    maintainers = [ maintainers.gp2112 ];
    platforms = platforms.all;
  };

}
