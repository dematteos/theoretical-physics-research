"""
class/scripts/run_class.py
--------------------------
Example script to run a CLASS simulation using the classy Python wrapper.
Computes CMB power spectra for a standard ΛCDM cosmology.
"""

import numpy as np
import matplotlib.pyplot as plt
from classy import Class

# ---- Cosmological parameters (Planck 2018 best-fit) ----
params = {
    'output':        'tCl,pCl,lCl',
    'l_max_scalars': 2500,
    'lensing':       'yes',
    'h':             0.6736,
    'omega_b':       0.02237,
    'omega_cdm':     0.1200,
    'A_s':           2.1e-9,
    'n_s':           0.9649,
    'tau_reio':      0.0544,
}

def run_simulation(params: dict) -> dict:
    """Run CLASS and return lensed Cls."""
    cosmo = Class()
    cosmo.set(params)
    cosmo.compute()
    cls = cosmo.lensed_cl(params['l_max_scalars'])
    cosmo.struct_cleanup()
    cosmo.empty()
    return cls


def plot_cls(cls: dict, output_path: str = "class/outputs/cls_TT.png"):
    """Plot TT power spectrum."""
    ell = cls['ell'][2:]
    TT  = cls['tt'][2:] * ell * (ell + 1) / (2 * np.pi) * 1e12  # μK²

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(ell, TT, color='steelblue', linewidth=1.5)
    ax.set_xlabel(r'Multipole $\ell$', fontsize=13)
    ax.set_ylabel(r'$\ell(\ell+1)C_\ell^{TT}/2\pi \; [\mu K^2]$', fontsize=13)
    ax.set_title('CMB TT Power Spectrum (ΛCDM)', fontsize=14)
    ax.set_xscale('log')
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    print(f"Plot saved to {output_path}")


if __name__ == "__main__":
    print("Running CLASS simulation...")
    cls = run_simulation(params)
    plot_cls(cls)
    print("Done.")
