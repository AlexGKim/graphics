#!/usr/bin/env python3
"""Generate left and right plots for wk_1.tex replacement."""

import numpy as np
import matplotlib.pyplot as plt

# Color scheme from TikZ slides
navybg = '#0d1b2a'
source1col = '#00dcff'  # cyan
source2col = '#ffa500'  # orange
thirdcol = '#64ff96'    # green
labelcol = '#dcdcdc'    # light grey
axiscol = '#b4b4b4'     # medium grey

# Figure setup
fig, (ax_left, ax_right) = plt.subplots(2, 1, figsize=(8, 12))
fig.patch.set_facecolor(navybg)

# ════════════════════════════════════════════════════════
# LEFT PLOT: S(ν) Line profiles
# ════════════════════════════════════════════════════════
nu = np.linspace(-4, 4, 1000)
nu0 = 0
delta_nu = 1.0

# Lorentzian: S(ν) ∝ 1 / (1 + ((ν-ν0)/σ)²)
lorentzian = delta_nu / (1 + (nu / delta_nu)**2)

# Gaussian: S(ν) ∝ exp(-(ν-ν0)²/(2σ²))
gaussian = np.exp(-(nu / delta_nu)**2 / 2)

# Tophat/rectangular: full width = 2*delta_nu to match FWHM of Lorentzian
tophat = np.where(np.abs(nu) <= delta_nu, 1.0, 0)

ax_left.plot(nu, lorentzian, color=source1col, linewidth=2.5, label='Lorentzian')
ax_left.plot(nu, gaussian, color=source2col, linewidth=2.5, label='Gaussian')
ax_left.plot(nu, tophat, color=thirdcol, linewidth=2.5, label='Tophat')

ax_left.set_facecolor(navybg)
ax_left.set_xlabel(r'$\nu - \nu_0$ ($\Delta\nu$ units)', color=labelcol, fontsize=14)
ax_left.set_ylabel(r'$S(\nu)$ (normalized)', color=labelcol, fontsize=14)
ax_left.set_xlim(-4, 4)
ax_left.set_ylim(-0.05, 1.1)
ax_left.spines['bottom'].set_color(axiscol)
ax_left.spines['left'].set_color(axiscol)
ax_left.spines['top'].set_visible(False)
ax_left.spines['right'].set_visible(False)
ax_left.tick_params(colors=labelcol, labelsize=12)
ax_left.legend(loc='upper right', framealpha=0.9, facecolor=navybg, edgecolor=axiscol,
               labelcolor=labelcol, fontsize=11)
ax_left.grid(True, alpha=0.2, color=axiscol)

# ════════════════════════════════════════════════════════
# RIGHT PLOT: |g^(1)(τ)| for each spectrum type
# ════════════════════════════════════════════════════════
tau = np.linspace(0, 8, 1000)
tau_c = 2.0  # coherence time

# Lorentzian spectrum → exponential g^(1): exp(-τ/τ_c)
g1_lorentzian = np.exp(-tau / tau_c)

# Gaussian spectrum → Gaussian g^(1): exp(-τ²/(2τ_c²))
g1_gaussian = np.exp(-(tau / tau_c)**2 / 2)

# Tophat spectrum → sinc g^(1): |sinc(πτ/τ_c)|
g1_tophat = np.abs(np.sinc(tau / tau_c))

ax_right.plot(tau, g1_lorentzian, color=source1col, linewidth=2.5, label='Lorentzian')
ax_right.plot(tau, g1_gaussian, color=source2col, linewidth=2.5, label='Gaussian')
ax_right.plot(tau, g1_tophat, color=thirdcol, linewidth=2.5, label='Tophat')

ax_right.set_facecolor(navybg)
ax_right.set_xlabel(r'$\tau$ ($\tau_c$ units)', color=labelcol, fontsize=14)
ax_right.set_ylabel(r'$|g^{(1)}(\tau)|$', color=labelcol, fontsize=14)
ax_right.set_xlim(0, 8)
ax_right.set_ylim(-0.05, 1.1)
ax_right.spines['bottom'].set_color(axiscol)
ax_right.spines['left'].set_color(axiscol)
ax_right.spines['top'].set_visible(False)
ax_right.spines['right'].set_visible(False)
ax_right.tick_params(colors=labelcol, labelsize=10)
ax_right.legend(loc='upper right', framealpha=0.9, facecolor=navybg, edgecolor=axiscol,
                labelcolor=labelcol, fontsize=11)
ax_right.grid(True, alpha=0.2, color=axiscol)

plt.tight_layout()
plt.savefig('figs/wk_plots.pdf', facecolor=navybg, edgecolor='none', dpi=300)
print("Saved figs/wk_plots.pdf")
plt.close()
