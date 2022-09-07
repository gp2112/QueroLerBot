{ lib, python310Packages, pkgs, callPackage, ... }:

let
  vnumber = "1.0.0";
  # manifest = (lib.importTOML ./pyproject.toml).project;
  telegraph = callPackage ./telegraph.nix {
    inherit (python310Packages) buildPythonPackage;
    inherit (pkgs.python310Packages) requests;
    inherit (pkgs.python310Packages) httpx;
    inherit (python310Packages) pytestCheckHook;
    inherit (python310Packages) pythonOlder;
  };
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
    telegraph
  ];

  meta = with lib; {
    description = "Um bot que dribla paywalls do twitter";
    homepage = "https://github.com/gp2112/querolerbot";
    license = licenses.agpl3;
    platforms = platforms.all;
  };

}
