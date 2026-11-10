#!/bin/bash
#SBATCH --job-name=MSH_GSE_HPC
#SBATCH --partition=skylake
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=40
#SBATCH --mem=128G
#SBATCH --time=01:00:00
#SBATCH --output=logs/msh_gse_%j.out
#SBATCH --error=logs/msh_gse_%j.err
# Optional multi-year array: #SBATCH --array=2008-2023

set -euo pipefail

mkdir -p logs output_nc data/omni_5min

# Prevent OpenBLAS / MKL / NumPy internal thread oversubscription across 40 multiprocessing workers
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

# Step 1: Compile Fortran shared library (libmsh.so) if not already built
if [ ! -f "./libmsh.so" ]; then
    echo "[Build] Compiling msh_core_lib.for -> libmsh.so ..."
    gfortran -O1 -fPIC -shared -ffixed-line-length-none msh_core_lib.for -o libmsh.so
fi

# Step 2: Determine target year (from Slurm array task ID, CLI arg, or default 2018)
TARGET_YEAR="${SLURM_ARRAY_TASK_ID:-${1:-2018}}"
TOTAL_CORES="${SLURM_CPUS_PER_TASK:-40}"

echo "=================================================================="
echo "Starting 40-Core GSE Magnetosheath Pipeline for Year=${TARGET_YEAR}"
echo "Node: $(hostname) | Allocated Cores: ${TOTAL_CORES}"
echo "=================================================================="

# Step 3: Run annual pipeline (12 monthly chunks, 3~4 workers per month, 40 total cores)
python3 hpc_pipeline.py \
    --year "${TARGET_YEAR}" \
    --total-cores "${TOTAL_CORES}" \
    --workers-per-month 3 \
    --concurrent-months 4 \
    --dx 0.5 \
    --out-dir "output_nc"

echo "=================================================================="
echo "Completed Year=${TARGET_YEAR} successfully at $(date -u)"
echo "=================================================================="
