"""
mcmc/scripts/run_mcmc.py
------------------------
MCMC parameter estimation using emcee + CLASS.
Fits H0 and omega_cdm to a mock CMB TT spectrum.
"""

import numpy as np
import emcee
import corner
import matplotlib.pyplot as plt
from classy import Class

# ---- Fiducial parameters (truth) ----
FIDUCIAL = {
    'output':        'tCl,lCl',
    'l_max_scalars': 1000,
    'lensing':       'yes',
    'h':             0.6736,
    'omega_b':       0.02237,
    'omega_cdm':     0.1200,
    'A_s':           2.1e-9,
    'n_s':           0.9649,
    'tau_reio':      0.0544,
}

L_MAX = 1000
ELL   = np.arange(2, L_MAX + 1)


def get_cls(h: float, omega_cdm: float) -> np.ndarray:
    """Compute TT Cls for given parameters."""
    params = FIDUCIAL.copy()
    params['h']         = h
    params['omega_cdm'] = omega_cdm
    cosmo = Class()
    cosmo.set(params)
    try:
        cosmo.compute()
        cls = cosmo.lensed_cl(L_MAX)['tt'][2:L_MAX+1]
    except Exception:
        cls = np.full(len(ELL), -np.inf)
    finally:
        cosmo.struct_cleanup()
        cosmo.empty()
    return cls


# ---- Generate mock data ----
print("Generating mock data...")
cls_fid  = get_cls(FIDUCIAL['h'], FIDUCIAL['omega_cdm'])
noise    = 0.05 * cls_fid
cls_data = cls_fid + noise * np.random.randn(len(ELL))


def log_likelihood(theta: np.ndarray) -> float:
    h, omega_cdm = theta
    cls_model    = get_cls(h, omega_cdm)
    if np.any(~np.isfinite(cls_model)):
        return -np.inf
    residuals = cls_data - cls_model
    return -0.5 * np.sum((residuals / noise) ** 2)


def log_prior(theta: np.ndarray) -> float:
    h, omega_cdm = theta
    if 0.5 < h < 0.9 and 0.08 < omega_cdm < 0.16:
        return 0.0
    return -np.inf


def log_prob(theta: np.ndarray) -> float:
    lp = log_prior(theta)
    if not np.isfinite(lp):
        return -np.inf
    return lp + log_likelihood(theta)


# ---- Run MCMC ----
NDIM     = 2
NWALKERS = 16
NSTEPS   = 500
LABELS   = [r'$h$', r'$\Omega_{cdm}$']

print(f"Starting MCMC: {NWALKERS} walkers, {NSTEPS} steps...")
p0 = np.array([FIDUCIAL['h'], FIDUCIAL['omega_cdm']]) + \
     1e-3 * np.random.randn(NWALKERS, NDIM)

sampler = emcee.EnsembleSampler(NWALKERS, NDIM, log_prob)
sampler.run_mcmc(p0, NSTEPS, progress=True)

# ---- Post-processing ----
tau    = sampler.get_autocorr_time(quiet=True)
burnin = int(2 * np.max(tau))
thin   = int(0.5 * np.min(tau))
flat_samples = sampler.get_chain(discard=burnin, thin=thin, flat=True)

print(f"\nAutocorrelation times: {tau}")
print(f"Burn-in: {burnin}, thin: {thin}")
print(f"Flat samples shape: {flat_samples.shape}")

for i, label in enumerate(LABELS):
    mcmc = np.percentile(flat_samples[:, i], [16, 50, 84])
    q    = np.diff(mcmc)
    print(f"{label} = {mcmc[1]:.4f} +{q[1]:.4f} -{q[0]:.4f}")

# ---- Corner plot ----
fig = corner.corner(flat_samples, labels=LABELS, truths=[FIDUCIAL['h'], FIDUCIAL['omega_cdm']])
fig.savefig("mcmc/plots/corner.png", dpi=150)
print("\nCorner plot saved to mcmc/plots/corner.png")
