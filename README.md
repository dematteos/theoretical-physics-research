# Theoretical Physics Research — dematteos

**HealthQE Research Center** | CNR · INFN · UPO

Simulations and analysis for theoretical physics research using CLASS (Cosmic Linear Anisotropy Solving System) and MCMC methods.

---

## Project Structure

```
theoretical-physics-research/
│
├── class/                  # CLASS simulations
│   ├── ini/                # Input parameter files (.ini)
│   ├── outputs/            # CLASS output data
│   └── scripts/            # Python scripts to run CLASS via classy
│
├── mcmc/                   # MCMC analysis
│   ├── chains/             # MCMC chain outputs
│   ├── configs/            # Config files (cobaya / MontePython)
│   ├── plots/              # Corner plots, triangle plots
│   └── scripts/            # Python scripts for MCMC runs and analysis
│
├── src/                    # Core C source code
│   ├── include/            # Header files (.h)
│   ├── lib/                # Compiled libraries
│   └── main.c              # Main C entry point
│
├── python/                 # Python utilities and analysis
│   ├── analysis/           # Post-processing, statistics
│   ├── plotting/           # Visualization scripts
│   └── utils/              # Helper functions
│
├── data/                   # Observational data (CMB, BAO, etc.)
│   ├── raw/                # Raw datasets
│   └── processed/          # Processed/cleaned datasets
│
├── notebooks/              # Jupyter notebooks for exploration
│
├── latex/                  # Paper drafts and notes
│   ├── paper/              # Main paper
│   └── notes/              # Research notes
│
├── tests/                  # Unit tests
│
├── setup.sh                # Environment setup script
├── requirements.txt        # Python dependencies
├── Makefile                # Build C code
└── README.md
```

---

## Requirements

### Python
- Python ≥ 3.9
- classy (Python wrapper for CLASS)
- cobaya or MontePython
- numpy, scipy, matplotlib
- getdist (for posterior plots)
- jupyter

### C
- gcc ≥ 9.0
- gsl (GNU Scientific Library)
- cfitsio (optional, for FITS file I/O)

---

## Setup

```bash
# Clone the repo
git clone https://github.com/dematteos/theoretical-physics-research.git
cd theoretical-physics-research

# Run setup
chmod +x setup.sh
./setup.sh
```

---

## Quickstart — CLASS simulation

```python
from classy import Class

cosmo = Class()
cosmo.set({
    'output': 'tCl,pCl,lCl',
    'l_max_scalars': 2500,
    'lensing': 'yes',
    'h': 0.6736,
    'omega_b': 0.02237,
    'omega_cdm': 0.1200,
    'A_s': 2.1e-9,
    'n_s': 0.9649,
    'tau_reio': 0.0544,
})
cosmo.compute()
cls = cosmo.lensed_cl(2500)
cosmo.struct_cleanup()
```

---

## Quickstart — MCMC with emcee

```python
import emcee
import numpy as np

# Define log-probability function
def log_prob(theta):
    h, omega_b, omega_cdm = theta
    if not (0.5 < h < 0.9): return -np.inf
    # ... compute likelihood with CLASS
    return log_likelihood + log_prior

sampler = emcee.EnsembleSampler(nwalkers=32, ndim=3, log_prob_fn=log_prob)
sampler.run_mcmc(initial_state, nsteps=1000, progress=True)
```

---

## References

- CLASS: [lesgourg.github.io/class_public](https://lesgourg.github.io/class_public/class.html)
- cobaya: [cobaya.readthedocs.io](https://cobaya.readthedocs.io)
- emcee: [emcee.readthedocs.io](https://emcee.readthedocs.io)
- MontePython: [baudren.github.io/montepython](http://baudren.github.io/montepython.html)

---

## Author

**Stefania De Matteo** — [@dematteos](https://github.com/dematteos)  
HealthQE Research Center | [www.healthqe.cloud](http://www.healthqe.cloud)
