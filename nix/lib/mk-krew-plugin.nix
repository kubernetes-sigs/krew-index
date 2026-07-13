{ lib, stdenvNoCC, fetchurl, unzip ? null }:

{
  pname,
  version ? "unknown",
  homepage ? "",
  shortDescription ? "",
  description ? "",
  platform,
}:

stdenvNoCC.mkDerivation rec {
  name = "${pname}-${version}";

  src = fetchurl {
    url = platform.uri;
    sha256 = platform.sha256;
  };

  nativeBuildInputs = lib.optionals (platform.archiveType == "zip") [ unzip ];

  dontConfigure = true;
  dontBuild = true;

  unpackPhase = ''
    runHook preUnpack

    case "${platform.archiveType}" in
      zip)
        unzip "$src"
        ;;
      tar.gz|tgz)
        tar -xzf "$src"
        ;;
      tar)
        tar -xf "$src"
        ;;
      none)
        cp "$src" ./downloaded-artifact
        ;;
      *)
        echo "Unsupported archiveType: ${platform.archiveType}" >&2
        exit 1
        ;;
    esac

    runHook postUnpack
  '';

  installPhase =
    let
      copyRules = platform.files or [ ];
      copyCommands = lib.concatMapStringsSep "\n" (
        rule:
        let
          from = rule.from;
          to = rule.to or ".";
        in
        ''
          copy_glob ${lib.escapeShellArg from} ${lib.escapeShellArg to}
        ''
      ) copyRules;
    in
    ''
      runHook preInstall

      pluginShareDir="$out/share/${pname}"
      mkdir -p "$out/bin" "$pluginShareDir"

      copy_glob() {
        local pattern="$1"
        local destination="$2"
        local targetDir
        local matchesFile

        if [[ "$destination" == "." ]]; then
          targetDir="$pluginShareDir"
        else
          targetDir="$pluginShareDir/$destination"
        fi

        mkdir -p "$targetDir"

        matchesFile="$(mktemp)"
        find . -path "./$pattern" ! -type d -print > "$matchesFile"

        if [[ ! -s "$matchesFile" ]]; then
          find . -path "./$pattern" -print > "$matchesFile"
        fi

        if [[ ! -s "$matchesFile" ]]; then
          rm -f "$matchesFile"
          echo "Pattern matched no files: $pattern" >&2
          exit 1
        fi

        while IFS= read -r matched; do
          cp -R "$matched" "$targetDir/"
        done < "$matchesFile"

        rm -f "$matchesFile"
      }

      ${copyCommands}

      binPath="${platform.bin}"

      if [[ -f "$pluginShareDir/$binPath" ]]; then
        install -m0755 "$pluginShareDir/$binPath" "$out/bin/$(basename "$binPath")"
      elif [[ -f "$binPath" ]]; then
        install -m0755 "$binPath" "$out/bin/$(basename "$binPath")"
      elif [[ -f ./downloaded-artifact ]]; then
        install -m0755 ./downloaded-artifact "$out/bin/$(basename "$binPath")"
      else
        binCandidate="$(find . -path "./$binPath" -print -quit)"
        if [[ -z "$binCandidate" ]]; then
          binCandidate="$(find . -name "$(basename "$binPath")" -print -quit)"
        fi

        if [[ -z "$binCandidate" ]]; then
          echo "Could not locate plugin binary: $binPath" >&2
          exit 1
        fi

        install -m0755 "$binCandidate" "$out/bin/$(basename "$binPath")"
      fi

      runHook postInstall
    '';

  meta =
    {
      description = if shortDescription != "" then shortDescription else description;
      mainProgram = builtins.baseNameOf platform.bin;
      sourceProvenance = [ lib.sourceTypes.binaryNativeCode ];
      platforms = [ platform.system ];
    }
    // lib.optionalAttrs (homepage != "") { inherit homepage; };
}
