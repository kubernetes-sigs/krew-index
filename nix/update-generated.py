#!/usr/bin/env python3

import argparse
import json
import pathlib
import sys
from typing import Any

try:
    import yaml
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Missing dependency: PyYAML. Run via `nix run .#update-generated` or install pyyaml."
    ) from exc


SYSTEMS = {
    "x86_64-linux": {"os": "linux", "arch": "amd64"},
    "aarch64-linux": {"os": "linux", "arch": "arm64"},
    "x86_64-darwin": {"os": "darwin", "arch": "amd64"},
    "aarch64-darwin": {"os": "darwin", "arch": "arm64"},
}


def normalize_archive_type(uri: str) -> str:
    lower = uri.lower().split("?", 1)[0].split("#", 1)[0]
    if lower.endswith(".tar.gz"):
        return "tar.gz"
    if lower.endswith(".tgz"):
        return "tgz"
    if lower.endswith(".tar"):
        return "tar"
    if lower.endswith(".zip"):
        return "zip"
    return "none"


def selector_matches(selector: dict[str, Any] | None, target: dict[str, str]) -> bool:
    if not selector:
        return True

    labels = selector.get("matchLabels") or {}
    for key in ("os", "arch"):
        value = labels.get(key)
        if value is not None and value != target[key]:
            return False

    expressions = selector.get("matchExpressions") or []
    for expr in expressions:
        key = expr.get("key")
        operator = expr.get("operator")
        values = expr.get("values") or []
        if key not in ("os", "arch"):
            continue

        target_value = target[key]
        if operator == "In" and target_value not in values:
            return False
        if operator == "NotIn" and target_value in values:
            return False
        if operator == "Exists" and target_value is None:
            return False
        if operator == "DoesNotExist":
            return False

    return True


def normalize_files(raw_files: Any) -> list[dict[str, str]]:
    files: list[dict[str, str]] = []
    for item in raw_files or []:
        if not isinstance(item, dict):
            continue
        src = item.get("from")
        if not src:
            continue
        files.append({"from": str(src), "to": str(item.get("to") or ".")})
    return files


def normalize_platform(platform: dict[str, Any], system: str) -> tuple[dict[str, Any] | None, str | None]:
    uri = platform.get("uri")
    sha256 = platform.get("sha256")
    binary = platform.get("bin")

    if not uri:
        return None, "platform missing uri"
    if not sha256:
        return None, "platform missing sha256"
    if not binary:
        return None, "platform missing bin"

    normalized = {
        "system": system,
        "uri": str(uri),
        "sha256": str(sha256),
        "bin": str(binary),
        "files": normalize_files(platform.get("files")),
        "archiveType": normalize_archive_type(str(uri)),
    }
    return normalized, None


def select_platform(platforms: list[dict[str, Any]], target: dict[str, str]) -> dict[str, Any] | None:
    for platform in platforms:
        if selector_matches(platform.get("selector"), target):
            return platform
    return None


def parse_manifest(path: pathlib.Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as stream:
        manifest = yaml.safe_load(stream)
    if not isinstance(manifest, dict):
        raise ValueError("manifest is not a mapping")
    return manifest


def build_metadata(plugins_dir: pathlib.Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "schemaVersion": 1,
        "systems": SYSTEMS,
        "plugins": {},
        "skipped": [],
    }

    for manifest_path in sorted(plugins_dir.glob("*.yaml")):
        try:
            manifest = parse_manifest(manifest_path)
        except Exception as exc:  # noqa: BLE001
            result["skipped"].append(
                {
                    "plugin": manifest_path.stem,
                    "system": "all",
                    "reason": f"invalid manifest: {exc}",
                }
            )
            continue

        plugin_name = ((manifest.get("metadata") or {}).get("name") or manifest_path.stem)
        spec = manifest.get("spec") or {}
        platforms = spec.get("platforms") or []

        if not isinstance(platforms, list) or not platforms:
            result["skipped"].append(
                {
                    "plugin": plugin_name,
                    "system": "all",
                    "reason": "spec.platforms missing or empty",
                }
            )
            continue

        plugin_info: dict[str, Any] = {
            "version": str(spec.get("version") or "unknown"),
            "homepage": str(spec.get("homepage") or ""),
            "shortDescription": str(spec.get("shortDescription") or ""),
            "description": str(spec.get("description") or ""),
            "platforms": {},
        }

        for system, target in SYSTEMS.items():
            selected = select_platform(platforms, target)
            if selected is None:
                result["skipped"].append(
                    {
                        "plugin": plugin_name,
                        "system": system,
                        "reason": "no matching platform selector",
                    }
                )
                continue

            normalized, error = normalize_platform(selected, system)
            if normalized is None:
                result["skipped"].append(
                    {
                        "plugin": plugin_name,
                        "system": system,
                        "reason": error,
                    }
                )
                continue

            plugin_info["platforms"][system] = normalized

        if plugin_info["platforms"]:
            result["plugins"][plugin_name] = plugin_info

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate normalized plugin metadata for Nix packaging.")
    parser.add_argument(
        "--plugins-dir",
        default="plugins",
        help="Directory with krew plugin manifests (*.yaml)",
    )
    parser.add_argument(
        "--out",
        default="nix/generated/plugins.json",
        help="Output JSON path",
    )
    args = parser.parse_args()

    repo_root = pathlib.Path(__file__).resolve().parents[1]
    plugins_dir = (repo_root / args.plugins_dir).resolve()
    output_path = (repo_root / args.out).resolve()

    if not plugins_dir.exists():
        print(f"Plugins directory not found: {plugins_dir}", file=sys.stderr)
        return 1

    metadata = build_metadata(plugins_dir)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as stream:
        json.dump(metadata, stream, indent=2, sort_keys=True)
        stream.write("\n")

    print(f"Generated {output_path}")
    print(f"Packaged plugins: {len(metadata['plugins'])}")
    print(f"Skipped entries: {len(metadata['skipped'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
