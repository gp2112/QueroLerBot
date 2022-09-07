{
  description = "Application packaged using poetry2nix";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs";

  outputs = { nixpkgs, ... }:
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
      overlays.default = final: prev: rec {
        ${name} = final.callPackage ./default.nix { };
      };

      packages = genSystems (system:
        let
          pkgs = import nixpkgs {
            inherit system;
            overlays = [ overlays.default ];
          };
        in
        rec {
          querolerbot = pkgs.${name};
          default = querolerbot;
        });


      nixosModules.default = import ./module.nix;
    };
}
