{
  description = "Nix packaging for krew-index plugins";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    nixpkgs-x86-darwin.url = "github:NixOS/nixpkgs/nixpkgs-26.05-darwin";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs =
    inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];

      perSystem =
        { system, ... }:
        let
          nixpkgsInput =
            if system == "x86_64-darwin" then
              inputs.nixpkgs-x86-darwin
            else
              inputs.nixpkgs;

          pkgs = import nixpkgsInput { inherit system; };
          inherit (pkgs) lib;

          metadata = builtins.fromJSON (builtins.readFile ./nix/generated/plugins.json);
          plugins = metadata.plugins or { };
          mkKrewPlugin = pkgs.callPackage ./nix/lib/mk-krew-plugin.nix { };
          updateGenerated = pkgs.writeShellApplication {
            name = "update-krew-nix-metadata";
            runtimeInputs = [
              pkgs.python3
              pkgs.python3Packages.pyyaml
            ];
            text = ''
              exec python3 ${./nix/update-generated.py} "$@"
            '';
          };

          pluginPackages = lib.mapAttrs'
            (
              pluginName: pluginMeta:
              let
                selectedPlatform = lib.attrByPath [ "platforms" system ] null pluginMeta;
              in
              lib.nameValuePair pluginName (
                mkKrewPlugin {
                  pname = pluginName;
                  version = pluginMeta.version or "unknown";
                  homepage = pluginMeta.homepage or "";
                  shortDescription = pluginMeta.shortDescription or "";
                  description = pluginMeta.description or "";
                  platform = selectedPlatform;
                }
              )
            )
            (lib.filterAttrs (_: pluginMeta: lib.attrByPath [ "platforms" system ] null pluginMeta != null) plugins);

          skippedForSystem = builtins.filter (item: item.system == system) (metadata.skipped or [ ]);
        in
        {
          packages = pluginPackages;

          apps.update-generated = {
            type = "app";
            program = "${updateGenerated}/bin/update-krew-nix-metadata";
          };

          formatter = pkgs.nixfmt-rfc-style;

          checks.metadata-summary = pkgs.runCommand "krew-nix-metadata-summary-${system}" {
            pluginCount = builtins.toString (builtins.length (builtins.attrNames pluginPackages));
            skippedCount = builtins.toString (builtins.length skippedForSystem);
          } ''
            mkdir -p "$out"
            {
              echo "system=${system}"
              echo "packaged_plugins=$pluginCount"
              echo "skipped_plugins=$skippedCount"
            } > "$out/summary.txt"
          '';
        };
    };
}
