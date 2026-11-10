#PBS -S /bin/bash
#PBS -N MSH_GSE_HPC
#PBS -l select=1:ncpus=40:model=sky_ele
#PBS -l walltime=02:00:00
#PBS -j oe
#PBS -W group_list=s3015
#PBS -m e
#PBS -q normal
##PBS -q devel

# Set stack size to unlimited for Fortran shared library and deep arrays
ulimit -s unlimited

# Load required compiler and system modules on NAS/Pleiades
module load comp-intel
module load pkgsrc python3

# Go to the submission working directory
cd "$PBS_O_WORKDIR"

# Create output and data directories
mkdir -p logs output_nc data/omni_5min

# Prevent OpenBLAS / MKL / NumPy thread oversubscription across 40 multiprocessing workers
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

# Step 1: Compile Fortran shared library (libmsh.so) if not present
if [ ! -f "./libmsh.so" ]; then
    echo "[Build] Compiling msh_core_lib.for -> libmsh.so ..."
    # If using ifort/icx from comp-intel:
    if command -v ifort >/dev/null 2>&1; then
        ifort -O2 -fPIC -shared -extend-source 132 msh_core_lib.for -o libmsh.so
    else
        gfortran -O1 -fPIC -shared -ffixed-line-length-none msh_core_lib.for -o libmsh.so
    fi
fi

# Step 2: Determine target year (Default: 2018 or pass via `qsub -v TARGET_YEAR=2019 PBS_MSheath.sh`)
TARGET_YEAR="${TARGET_YEAR:-2018}"
TOTAL_CORES=40

OMNI_LOCAL_PATH="data/omni_5min/omni_5min${TARGET_YEAR}.asc"
if [ ! -f "${OMNI_LOCAL_PATH}" ]; then
    echo "=================================================================="
    echo "[ERROR] OMNI 5-min data file not found: ${OMNI_LOCAL_PATH}"
    echo "Pleiades compute nodes cannot download files from external internet."
    echo "Please download the data on the login node (pfe) first by running:"
    echo "   bash download_omni.sh ${TARGET_YEAR}"
    echo "=================================================================="
    exit 1
fi

echo "=================================================================="
echo "Job ID: ${PBS_JOBID}"
echo "Running on Host: $(hostname)"
echo "Target Year: ${TARGET_YEAR} | Total Cores: ${TOTAL_CORES}"
echo "Start Time: $(date -u)"
echo "=================================================================="

# Step 3: Run 40-Core HPC GSE Magnetosheath Pipeline
# - 12 Monthly Chunks (YYYY-01 to YYYY-12)
# - 4 Concurrent Months in parallel wave, ~10 workers per month across 40 cores
# - 0.5 Re grid resolution
python3 hpc_pipeline.py \
    --year "${TARGET_YEAR}" \
    --total-cores "${TOTAL_CORES}" \
    --workers-per-month 3 \
    --concurrent-months 4 \
    --dx 0.5 \
    --out-dir "output_nc"

echo "=================================================================="
echo "Completed Job for Year=${TARGET_YEAR} at $(date -u)"
echo "Outputs generated in: ${PBS_O_WORKDIR}/output_nc"
echo "=================================================================="
