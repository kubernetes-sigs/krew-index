# Nix support for plugin builds

This repository exposes Nix packages for Krew plugins using `flake-parts` + `nixpkgs`.

## How it works

- Plugin manifests are sourced from `plugins/*.yaml`.
- A generator script normalizes the manifests into `nix/generated/plugins.json`.
- `flake.nix` reads the JSON and creates `packages.<plugin-name>` dynamically.

Current target systems:

- `x86_64-linux`
- `aarch64-linux`

## Update metadata

Regenerate metadata after manifest changes:

```bash
nix run .#update-generated
```

The command updates `nix/generated/plugins.json`.

## Build a plugin

Build one plugin package:

```bash
nix build .#stern
```

List generated packages:

```bash
nix flake show
```

## Notes

- Only platform entries matching the current Nix `system` are packaged.
- Non-matching/invalid platform entries are tracked in `nix/generated/plugins.json` under `skipped`.
