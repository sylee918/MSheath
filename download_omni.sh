#!/bin/bash
# ==============================================================================
# download_omni.sh
# Run this script on the NASA Pleiades login/frontend node (pfe),
# where external Internet access is available.
# Compute nodes (PBS batch jobs) do NOT have outbound internet access.
# ==============================================================================

set -euo pipefail

YEAR="${1:-2018}"
DEST_DIR="data/omni_5min"
mkdir -p "${DEST_DIR}"

DEST_FILE="${DEST_DIR}/omni_5min${YEAR}.asc"
URL="https://spdf.gsfc.nasa.gov/pub/data/omni/high_res_omni/omni_5min${YEAR}.asc"

if [ -f "${DEST_FILE}" ] && [ -s "${DEST_FILE}" ]; then
    echo "[download_omni] ${DEST_FILE} already exists ($(du -h "${DEST_FILE}" | cut -f1)). Skipping download."
    exit 0
fi

echo "[download_omni] Downloading OMNI 5-min data for Year=${YEAR} from NASA SPDF..."
echo "  URL: ${URL}"
echo "  Destination: ${DEST_FILE}"

if command -v curl >/dev/null 2>&1; then
    curl -f -L "${URL}" -o "${DEST_FILE}"
elif command -v wget >/dev/null 2>&1; then
    wget "${URL}" -O "${DEST_FILE}"
else
    python3 -c "import urllib.request; urllib.request.urlretrieve('${URL}', '${DEST_FILE}')"
fi

echo "[download_omni] Successfully downloaded Year=${YEAR} ($(du -h "${DEST_FILE}" | cut -f1))"
