{
  description = "Application packaged using poetry2nix";

  inputs.utils.url = "github:numtide/flake-utils";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs";

  outputs = inputs @ { self, nixpkgs, utils, ... }:
  let
    inherit (nixpkgs) lib;
    pkgsFor = nixpkgs.legacyPackages;
    name = "querolerbot";
    genSystems = lib.genAttrs [
      "aarch64-linux"
      "x86_64-linux"
    ];
  in
  rec {
    overlays.default = _: prev: rec {
      ${name} = prev.callPackage ./default.nix {};
    };

    packages = genSystems (system:
      (self.overlays.default null pkgsFor.${system})
      // {
        default = self.packages.${system}.${name};
      });


    nixosModules.default = import ./module.nix;
  };
}
