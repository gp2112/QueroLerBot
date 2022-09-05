{ lib, python310Packages, pkgs, ... }:

let
  vnumber = "1.0.0";
  # manifest = (lib.importTOML ./pyproject.toml).project;
in
python310Packages.buildPythonPackage rec {

  imports = [
    ./telegraph.nix
  ];

  pname = "querolerbot";
  version = "${vnumber}-beta";

  format = "pyproject";

  src = ./.;

  propagatedBuildInputs = with pkgs.python310Packages; [
    requests
    toml
    beautifulsoup4
    requests-oauthlib
  ];

  meta = with lib; {
    description = "Um bot que dribla paywalls do twitter";
    homepage = "https://github.com/gp2112/querolerbot";
    license = licenses.agpl3;
    platforms = platforms.all;
  };

}
