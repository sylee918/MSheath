#PBS -S /bin/bash
#PBS -N MSH_GSE_HPC
#PBS -l select=1:ncpus=40:model=sky_ele
#PBS -l walltime=02:00:00
#PBS -j oe
#PBS -W group_list=s3015
#PBS -m e
##PBS -q normal
#PBS -q devel

# Set stack size to unlimited for Fortran shared library and deep arrays
ulimit -s unlimited

# Load required compiler and system modules on NAS/Pleiades
module load comp-intel
module load pkgsrc python3

# Go to the submission working directory
cd "$PBS_O_WORKDIR"

# Create output and data directories
mkdir -p logs output_nc summary_stats data/omni_5min

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

# Step 2: Determine target years (Default: "2018 2025", or pass TARGET_YEAR=2019 / TARGET_YEARS="2018 2025")
TARGET_YEARS="${TARGET_YEARS:-${TARGET_YEAR:-2018 2025}}"
TOTAL_CORES=40

# Pre-flight check: verify all OMNI data files exist before starting compute
for YR in ${TARGET_YEARS}; do
    OMNI_LOCAL_PATH="data/omni_5min/omni_5min${YR}.asc"
    if [ ! -f "${OMNI_LOCAL_PATH}" ]; then
        echo "=================================================================="
        echo "[ERROR] OMNI 5-min data file not found: ${OMNI_LOCAL_PATH}"
        echo "Pleiades compute nodes cannot download files from external internet."
        echo "Please download the data on the login node (pfe) first by running:"
        echo "   bash download_omni.sh ${YR}"
        echo "=================================================================="
        exit 1
    fi
done

echo "=================================================================="
echo "Job ID: ${PBS_JOBID}"
echo "Running on Host: $(hostname)"
echo "Target Years: ${TARGET_YEARS} | Total Cores: ${TOTAL_CORES}"
echo "Start Time: $(date -u)"
echo "=================================================================="

# Step 3: Run 40-Core HPC GSE 3D Magnetosheath Pipeline + 3D Summary Builder sequentially
for YR in ${TARGET_YEARS}; do
    echo "------------------------------------------------------------------"
    echo "[Year ${YR}] Starting 3D MSheath pipeline at $(date -u)"
    echo "------------------------------------------------------------------"
    python3 hpc_pipeline.py \
        --year "${YR}" \
        --total-cores "${TOTAL_CORES}" \
        --workers-per-month 10 \
        --concurrent-months 4 \
        --dx 0.5 \
        --xmin -10.0 --xmax 20.0 \
        --ymin -25.0 --ymax 25.0 \
        --zmin -15.0 --zmax 15.0 \
        --out-dir "output_nc" || exit 1

    echo "[Year ${YR}] Building 3D Annual/Monthly Summary NetCDF4..."
    python3 build_summary_stats.py \
        --in-dir "output_nc" \
        --year "${YR}" \
        --stats-only \
        --out "summary_stats/MSH_GSE_${YR}_3D_Summary.nc" || exit 1
done

echo "=================================================================="
echo "Completed Job for Years=[${TARGET_YEARS}] at $(date -u)"
echo "Monthly Outputs : ${PBS_O_WORKDIR}/output_nc"
echo "3D Summaries    : ${PBS_O_WORKDIR}/summary_stats"
echo "=================================================================="
