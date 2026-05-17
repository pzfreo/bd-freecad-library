#!/usr/bin/env bash
# Regenerate all standards modules from their family manifests.
#
# Requires:
#   - ``../fcd2b123d`` checked out (the translator + family_extract)
#   - ``FCSTD2B123D_FREECAD_PYTHON`` pointing at a FreeCAD-enabled Python
#   - ``FCSTD2B123D_FREECAD_PYTHONPATH`` set (FreeCAD lib path)
#
# Run from the repo root:
#   ./tools/regenerate.sh
#
# Or pass a single manifest:
#   ./tools/regenerate.sh families/en_10058.yaml

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FCSTD2B123D_REPO="${FCSTD2B123D_REPO:-${REPO_ROOT}/../fcd2b123d}"

if [[ ! -d "${FCSTD2B123D_REPO}/src/fcstd2b123d" ]]; then
  echo "error: fcstd2b123d checkout not found at ${FCSTD2B123D_REPO}" >&2
  echo "set FCSTD2B123D_REPO to point at the translator repo" >&2
  exit 1
fi

if [[ -z "${FCSTD2B123D_FREECAD_PYTHON:-}" ]]; then
  echo "error: FCSTD2B123D_FREECAD_PYTHON not set (FreeCAD-enabled Python)" >&2
  exit 1
fi

# Manifests to process. Specific manifest if passed, otherwise all.
MANIFESTS=()
if [[ $# -gt 0 ]]; then
  MANIFESTS=("$@")
else
  while IFS= read -r m; do
    MANIFESTS+=("$m")
  done < <(find "${REPO_ROOT}/families" -name '*.yaml' -type f | sort)
fi

PYTHONPATH="${FCSTD2B123D_REPO}/src" \
FCSTD2B123D_FREECAD_PYTHONPATH="${FCSTD2B123D_FREECAD_PYTHONPATH}" \
PY="${FCSTD2B123D_FREECAD_PYTHON}"

for manifest in "${MANIFESTS[@]}"; do
  family="$(basename "${manifest}" .yaml)"
  output="${REPO_ROOT}/src/bd_freecad_library/standards/${family}.py"
  echo "Regenerating ${family} → ${output}"
  PYTHONPATH="${FCSTD2B123D_REPO}/src" \
  python3 -m fcstd2b123d.family_extract \
      "${manifest}" \
      --fixtures-root "${FCSTD2B123D_REPO}/tests/fixtures" \
      -o "${output}"
done

echo
echo "All manifests regenerated. Review with 'git diff src/bd_freecad_library/standards/'."
