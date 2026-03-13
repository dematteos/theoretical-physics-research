/*
 * src/main.c
 * ----------
 * Main entry point for C numerical computations.
 * Example: matter power spectrum integration using GSL.
 *
 * Compile: make
 * Run:     ./bin/main
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <gsl/gsl_integration.h>
#include "include/cosmology.h"

/* ---- ΛCDM transfer function approximation (Bardeen et al. 1986) ---- */
double transfer_function(double k, void *params) {
    cosmo_params *p = (cosmo_params *)params;
    double q   = k / (p->Omega_m * p->h * p->h) * exp(p->Omega_b + sqrt(2.0 * p->h) * p->Omega_b / p->Omega_m);
    double T   = log(1.0 + 2.34 * q) / (2.34 * q) *
                 pow(1.0 + 3.89*q + pow(16.1*q,2) + pow(5.46*q,3) + pow(6.71*q,4), -0.25);
    return T;
}

/* ---- Matter power spectrum P(k) ---- */
double matter_power_spectrum(double k, cosmo_params *p) {
    double T   = transfer_function(k, p);
    double P_k = p->A_s * pow(k / p->k_pivot, p->n_s - 1.0) * k * T * T;
    return P_k;
}

int main(void) {
    printf("=== Theoretical Physics Research ===\n");
    printf("    HealthQE Research Center\n\n");

    /* --- Set cosmological parameters --- */
    cosmo_params p;
    p.h       = 0.6736;
    p.Omega_m = 0.3153;
    p.Omega_b = 0.04930;
    p.A_s     = 2.1e-9;
    p.n_s     = 0.9649;
    p.k_pivot = 0.05;   /* Mpc^-1 */

    /* --- Compute P(k) over a range of k --- */
    int    N_k  = 100;
    double k_min = 1e-4;
    double k_max = 10.0;
    double dk    = (log(k_max) - log(k_min)) / (N_k - 1);

    printf("k [Mpc^-1]      P(k) [Mpc^3]\n");
    printf("-------------------------------\n");

    for (int i = 0; i < N_k; i++) {
        double k = exp(log(k_min) + i * dk);
        double P = matter_power_spectrum(k, &p);
        if (i % 10 == 0)
            printf("  %.4e      %.4e\n", k, P);
    }

    printf("\nDone.\n");
    return EXIT_SUCCESS;
}
