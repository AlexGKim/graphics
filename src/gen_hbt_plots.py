#!/usr/bin/env python3
"""Generate histogram and g^(2)(0,B) plots for hbt_1–hbt_4.tex."""

import numpy as np
import matplotlib.pyplot as plt

navybg   = '#0d1b2a'
histcol  = '#64b4ff'
ocol     = '#ffa500'
labelcol = '#dcdcdc'
axiscol  = '#b4b4b4'


def style_ax(ax):
    ax.set_facecolor(navybg)
    ax.spines['bottom'].set_color(axiscol)
    ax.spines['left'].set_color(axiscol)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(colors=labelcol, labelsize=12)


def make_histogram(ax, mu2, seed=42):
    """Draw H(τ) bars + uncorrelated baseline on ax. mu2 = |μ(B)|²."""
    tau_c = 1.5
    tau_obs = 5.0
    bin_width = 0.3
    bins = np.arange(0, 6.5, bin_width)
    tau_centers = bins + bin_width / 2

    H_uncorr = np.exp(-tau_centers / tau_obs)
    g2 = 1 + mu2 * np.exp(-(tau_centers / tau_c) ** 2)
    H = H_uncorr * g2

    rng = np.random.default_rng(seed)
    scale = 2000
    H_counts = rng.poisson(H * scale) / scale

    ax.bar(bins, H_counts, width=bin_width, align='edge',
           color=histcol, alpha=0.85, edgecolor='none')

    tau_smooth = np.linspace(0, 6.5, 300)
    H_uncorr_smooth = np.exp(-tau_smooth / tau_obs)
    ax.plot(tau_smooth, H_uncorr_smooth, color=axiscol, lw=1.5,
            linestyle='--', label='uncorrelated')
    ax.text(6.3, H_uncorr_smooth[-1] + 0.04, 'uncorrelated',
            color=axiscol, fontsize=10, ha='right', va='bottom')

    ax.set_xlabel(r'$\tau$', color=labelcol, fontsize=14)
    ax.set_ylabel(r'$H(\tau)$', color=labelcol, fontsize=14)
    ax.set_xlim(0, 6.5)
    ax.set_yticks([])
    style_ax(ax)


# ════════════════════════════════════════════════════════
# 1. hbt_hist.pdf  — single chaotic histogram (hbt_1, hbt_2, hbt_3)
# ════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(6, 3.5))
fig.patch.set_facecolor(navybg)
make_histogram(ax, mu2=1.0)
plt.tight_layout()
plt.savefig('figs/hbt_hist.pdf', facecolor=navybg, edgecolor='none', dpi=300)
print("Saved figs/hbt_hist.pdf")
plt.close()

# ════════════════════════════════════════════════════════
# 2. hbt_g2_0B.pdf  — g^(2)(0,B)−1 vs B  (hbt_4 left panel)
# ════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(5, 4))
fig.patch.set_facecolor(navybg)

u = np.linspace(0, 4, 1000)
g2_minus1 = np.sinc(u) ** 2   # sinc²(πu)/π² ... np.sinc includes the π factor

ax.plot(u, g2_minus1, color=histcol, lw=2.5)

B1, B2 = 0.4, 1.5
for Bu, color, label in [(B1, histcol, r'$B_1$'), (B2, ocol, r'$B_2$')]:
    val = np.sinc(Bu) ** 2
    ax.axvline(Bu, color=color, lw=1.2, linestyle='--', alpha=0.8)
    ax.plot(Bu, val, 'o', color=color, markersize=8)
    offset = (0.07, 0.03) if Bu == B1 else (-0.12, 0.03)
    ax.text(Bu + offset[0], val + offset[1], label,
            color=color, fontsize=12, va='bottom')

# Half-max annotation
ax.axhline(0.5, xmin=0, xmax=1/4, color='white', lw=0.8, alpha=0.6)
ax.text(0.05, 0.52, r'$\propto 1/\theta_s$', color='white', fontsize=10)

ax.set_xlabel(r'$B$', color=labelcol, fontsize=14)
ax.set_ylabel(r'$g^{(2)}(0,B)-1$', color=labelcol, fontsize=14)
ax.set_xlim(0, 4)
ax.set_ylim(-0.05, 1.1)
ax.set_xticks([0, 1, 2, 3, 4])
ax.set_xticklabels(['0', '1', '2', '3', '4'])
style_ax(ax)

plt.tight_layout()
plt.savefig('figs/hbt_g2_0B.pdf', facecolor=navybg, edgecolor='none', dpi=300)
print("Saved figs/hbt_g2_0B.pdf")
plt.close()

# ════════════════════════════════════════════════════════
# 3. hbt_hist_dual.pdf  — two overlapping histograms at B1, B2 (hbt_4 right panel)
# ════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(6, 4))
fig.patch.set_facecolor(navybg)

mu2_B1 = np.sinc(B1) ** 2   # ≈ 0.73
mu2_B2 = np.sinc(B2) ** 2   # ≈ 0.045

make_histogram(ax, mu2=mu2_B1, seed=42)

# Overlay B2 histogram (different seed to vary noise)
tau_c = 1.5
tau_obs = 8.0
bin_width = 0.3
bins = np.arange(0, 4.5, bin_width)
tau_centers = bins + bin_width / 2
H_uncorr = np.exp(-tau_centers / tau_obs)
g2_B2 = 1 + mu2_B2 * np.exp(-(tau_centers / tau_c) ** 2)
H_B2 = H_uncorr * g2_B2
rng2 = np.random.default_rng(7)
scale = 300
H_B2_counts = rng2.poisson(H_B2 * scale) / scale
ax.bar(bins, H_B2_counts, width=bin_width, align='edge',
       color=ocol, alpha=0.7, edgecolor='none')

# Re-draw uncorrelated line on top
tau_smooth = np.linspace(0, 6.5, 300)
ax.plot(tau_smooth, np.exp(-tau_smooth / tau_obs), color=axiscol, lw=1.5, linestyle='--')

# Legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=histcol, alpha=0.85, label=r'$B_1$'),
                   Patch(facecolor=ocol,    alpha=0.70, label=r'$B_2$')]
ax.legend(handles=legend_elements, loc='upper right', framealpha=0.85,
          facecolor=navybg, edgecolor=axiscol, labelcolor=labelcol, fontsize=12)

plt.tight_layout()
plt.savefig('figs/hbt_hist_dual.pdf', facecolor=navybg, edgecolor='none', dpi=300)
print("Saved figs/hbt_hist_dual.pdf")
plt.close()
