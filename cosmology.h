/*
 * src/include/cosmology.h
 * -----------------------
 * Data structures and function prototypes for cosmological computations.
 */

#ifndef COSMOLOGY_H
#define COSMOLOGY_H

/* ---- Cosmological parameters struct ---- */
typedef struct {
    double h;        /* Dimensionless Hubble parameter H0/100 */
    double Omega_m;  /* Total matter density parameter */
    double Omega_b;  /* Baryon density parameter */
    double Omega_L;  /* Dark energy density parameter */
    double A_s;      /* Scalar amplitude */
    double n_s;      /* Spectral index */
    double k_pivot;  /* Pivot scale [Mpc^-1] */
    double tau_reio; /* Optical depth to reionization */
} cosmo_params;

/* ---- Function prototypes ---- */
double transfer_function(double k, void *params);
double matter_power_spectrum(double k, cosmo_params *p);

#endif /* COSMOLOGY_H */
