{
  description = "Application packaged using poetry2nix";

  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs";
  inputs.poetry2nix.url = "github:nix-community/poetry2nix";



  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    let
      name = "querolerbot";
    in
    rec {
      nixosModules."${name}" = import ./module.nix;
      nixosModule = nixosModules."${name}";

      # Nixpkgs overlay providing the application
      overlays.default = _: prev {
          # The application
          ${name} = prev.callPackage ./default.nix {};
        };
    } // (flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ self.overlay ];
        };
      in
      {
        apps = {
          ${name} = pkgs.${name};
        };

        defaultApp = pkgs.${name};

        # build
        packages.${name} = pkgs.${name};

      }));
}
