#!/bin/bash
# ============================================================
# setup.sh — Environment setup for theoretical-physics-research
# Tested on Ubuntu 22.04 / macOS 13+
# ============================================================

set -e
echo "=============================================="
echo "  HealthQE Research — Environment Setup"
echo "=============================================="

# --- 1. System dependencies ---
echo ""
echo "[1/5] Installing system dependencies..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt-get update -qq
    sudo apt-get install -y \
        gcc g++ gfortran make cmake \
        libgsl-dev libfftw3-dev \
        libcfitsio-dev libhdf5-dev \
        python3 python3-pip python3-venv \
        git wget curl
elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew install gcc gsl fftw cfitsio hdf5 python3
fi

# --- 2. Python virtual environment ---
echo ""
echo "[2/5] Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip setuptools wheel

# --- 3. Python packages ---
echo ""
echo "[3/5] Installing Python packages..."
pip install \
    numpy scipy matplotlib \
    classy \
    emcee cobaya \
    getdist corner \
    astropy healpy \
    jupyter ipykernel \
    tqdm h5py pandas \
    pytest

# --- 4. Install CLASS (optional full build) ---
echo ""
echo "[4/5] Cloning CLASS..."
if [ ! -d "class_public" ]; then
    git clone https://github.com/lesgourg/class_public.git
    cd class_public
    make
    cd ..
    echo "  CLASS built successfully."
else
    echo "  CLASS already present, skipping."
fi

# --- 5. Create directory structure ---
echo ""
echo "[5/5] Creating project directory structure..."
mkdir -p class/ini class/outputs class/scripts
mkdir -p mcmc/chains mcmc/configs mcmc/plots mcmc/scripts
mkdir -p src/include src/lib
mkdir -p python/analysis python/plotting python/utils
mkdir -p data/raw data/processed
mkdir -p notebooks
mkdir -p latex/paper latex/notes
mkdir -p tests

# Create placeholder files
touch class/ini/.gitkeep
touch mcmc/chains/.gitkeep
touch data/raw/.gitkeep

echo ""
echo "=============================================="
echo "  Setup complete!"
echo "  Activate environment with: source venv/bin/activate"
echo "=============================================="
