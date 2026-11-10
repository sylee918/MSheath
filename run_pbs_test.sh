#PBS -S /bin/bash
#PBS -N MSH_TEST
#PBS -l select=1:ncpus=8:model=sky_ele
#PBS -l walltime=00:10:00
#PBS -j oe
#PBS -W group_list=s3015
#PBS -m e
#PBS -q devel

# Quick Test Script on NASA Pleiades (runs in < 1 minute on `devel` queue)
ulimit -s unlimited

module load comp-intel
module load pkgsrc python3

cd "$PBS_O_WORKDIR"
mkdir -p logs test_nc data/omni_5min

export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1

# Compile if not present
if [ ! -f "./libmsh.so" ]; then
    if command -v ifort >/dev/null 2>&1; then
        ifort -O2 -fPIC -shared -extend-source 132 msh_core_lib.for -o libmsh.so
    else
        gfortran -O1 -fPIC -shared -ffixed-line-length-none msh_core_lib.for -o libmsh.so
    fi
fi

echo "=================================================================="
echo "Starting Quick Verification Test on Host: $(hostname)"
echo "Queue: devel | Allocated Cores: 8"
echo "=================================================================="

# Test 1: Run automated verification suite (accuracy, coord transforms, NetCDF4)
echo ">>> Running test_hpc_pipeline.py ..."
python3 test_hpc_pipeline.py

# Test 2: Quick pipeline run for 1 month, capped at 288 steps (1 day)
echo ">>> Running quick pipeline benchmark (288 steps) ..."
LOCAL_OMNI="data/omni_5min/omni_5min2018.asc"
if [ -f "${LOCAL_OMNI}" ]; then
    OMNI_ARG="--omni-file ${LOCAL_OMNI}"
else
    OMNI_ARG="--omni-file SYNTHETIC"
fi

python3 hpc_pipeline.py \
    --year 2018 \
    --months 1 \
    --total-cores 8 \
    --workers-per-month 8 \
    --concurrent-months 1 \
    --max-steps 288 \
    --dx 0.5 \
    --out-dir "test_nc" \
    ${OMNI_ARG}

echo "=================================================================="
echo "Quick Test Completed Successfully at $(date -u)"
echo "Output NetCDF file check:"
ls -lh test_nc/*.nc
echo "=================================================================="
