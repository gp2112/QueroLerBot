{ lib, python310Packages, pkgs, callPackage, ... }:

let
  vnumber = "1.0.0";
in
python310Packages.buildPythonPackage rec {

  pname = "querolerbot";
  version = "${vnumber}-beta";

  format = "pyproject";

  src = ./.;

  propagatedBuildInputs = with pkgs.python310Packages; [
    requests
    toml
    beautifulsoup4
    requests-oauthlib
    telegraph
  ];

  meta = with lib; {
    description = "Um bot que dribla paywalls do twitter";
    homepage = "https://github.com/gp2112/querolerbot";
    license = licenses.agpl3;
    platforms = platforms.all;
  };

}
