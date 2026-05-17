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
    ax.tick_params(colors=labelcol, labelsize=18)


TAU_C   = 1.5
TAU_OBS = 5.0
TAU_MAX = 6.5
BIN_W   = 0.3
SCALE   = 2000
G2_YMAX = 2.2


def make_histogram(ax, mu2, color=histcol, alpha=0.85, seed=42):
    """Draw H(τ)/H_uncorr(0) bars + baseline on ax. y-axis is on g^(2) scale."""
    bins = np.arange(0, TAU_MAX, BIN_W)
    tau_centers = bins + BIN_W / 2

    H_uncorr = np.exp(-tau_centers / TAU_OBS)   # H_uncorr(0) = 1
    g2 = 1 + mu2 * np.exp(-(tau_centers / TAU_C) ** 2)
    H = H_uncorr * g2   # already normalised: H(0) = g^(2)(0,B)

    rng = np.random.default_rng(seed)
    H_counts = rng.poisson(H * SCALE) / SCALE

    ax.bar(bins, H_counts, width=BIN_W, align='edge',
           color=color, alpha=alpha, edgecolor='none')

    tau_smooth = np.linspace(0, TAU_MAX, 300)
    baseline = np.exp(-tau_smooth / TAU_OBS)
    return baseline, tau_smooth


# ════════════════════════════════════════════════════════
# 1. hbt_hist.pdf  — single chaotic histogram (hbt_1, hbt_2, hbt_3)
# ════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(6, 3.5))
fig.patch.set_facecolor(navybg)
baseline, tau_smooth = make_histogram(ax, mu2=1.0)
uncorr_line, = ax.plot(tau_smooth, baseline, color='black', lw=3, linestyle='--', label='uncorrelated')
ax.set_xlabel(r'$\tau$', color=labelcol, fontsize=21)
ax.set_ylabel(r'$H(\tau)$', color=labelcol, fontsize=21)
ax.set_xlim(0, TAU_MAX)
ax.set_ylim(0, G2_YMAX)
ax.set_yticks([])
ax.legend(handles=[uncorr_line], loc='upper right', framealpha=0.85,
          facecolor=navybg, edgecolor=axiscol, labelcolor=labelcol, fontsize=17)
style_ax(ax)
plt.tight_layout()
plt.savefig('figs/hbt_hist.pdf', facecolor=navybg, edgecolor='none', dpi=300)
print("Saved figs/hbt_hist.pdf")
plt.close()

B1, B2 = 0.4, 1.5
mu2_B1 = np.sinc(B1) ** 2   # ≈ 0.73
mu2_B2 = np.sinc(B2) ** 2   # ≈ 0.045

# g^(2)(0) values for B1 and B2 — these are the y-positions the dots must match
g2_0_B1 = 1 + mu2_B1   # ≈ 1.73
g2_0_B2 = 1 + mu2_B2   # ≈ 1.045

# ════════════════════════════════════════════════════════
# 2. hbt_g2_0B.pdf  — g^(2)(0,B) vs B  (hbt_4 left panel)
# y-axis on same g^(2) scale [0, G2_YMAX] as right panel
# ════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(5, 4))
fig.patch.set_facecolor(navybg)

u = np.linspace(0, 4, 1000)
g2m1 = np.sinc(u) ** 2   # g^(2)(0,B) - 1 = sinc²(πu)

ax.plot(u, g2m1, color=histcol, lw=2.5)

for Bu, color, label in [(B1, histcol, r'$B_1$'), (B2, ocol, r'$B_2$')]:
    val = np.sinc(Bu) ** 2
    ax.axvline(Bu, color=color, lw=1.2, linestyle='--', alpha=0.8)
    ax.plot(Bu, val, 'o', color=color, markersize=8)
    offset = (0.07, 0.03) if Bu == B1 else (-0.15, 0.03)
    ax.text(Bu + offset[0], val + offset[1], label,
            color=color, fontsize=18, va='bottom')

# Half-max annotation: find exact half-max of sinc²(πu)
u_halfmax = u[np.argmin(np.abs(g2m1[:500] - 0.5))]
ax.annotate('', xy=(u_halfmax, 0.5), xytext=(0, 0.5),
            arrowprops=dict(arrowstyle='<->', color='white', lw=1.5))
ax.text(u_halfmax / 2, 0.54, r'$\propto 1/\theta_s$',
        color='white', fontsize=15, ha='center', va='bottom')

ax.set_xlabel(r'$B$', color=labelcol, fontsize=21)
ax.set_ylabel(r'$g^{(2)}(0,B)-1$', color=labelcol, fontsize=21)
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
from matplotlib.patches import Patch

fig, ax = plt.subplots(figsize=(6, 4))
fig.patch.set_facecolor(navybg)

# B1 histogram
baseline, tau_smooth = make_histogram(ax, mu2=mu2_B1, color=histcol, alpha=0.85, seed=42)
# B2 histogram
make_histogram(ax, mu2=mu2_B2, color=ocol, alpha=0.7, seed=7)

# Shared baseline on top
from matplotlib.lines import Line2D
uncorr_line = Line2D([0], [0], color='black', lw=3, linestyle='--', label='uncorrelated')
ax.plot(tau_smooth, baseline, color='black', lw=3, linestyle='--')

legend_elements = [Patch(facecolor=histcol, alpha=0.85, label=r'$B_1$'),
                   Patch(facecolor=ocol,    alpha=0.70, label=r'$B_2$'),
                   uncorr_line]
ax.legend(handles=legend_elements, loc='upper right', framealpha=0.85,
          facecolor=navybg, edgecolor=axiscol, labelcolor=labelcol, fontsize=18)

ax.set_xlabel(r'$\tau$', color=labelcol, fontsize=21)
ax.set_ylabel(r'$H(\tau)$', color=labelcol, fontsize=21)
ax.set_xlim(0, TAU_MAX)
ax.set_ylim(0, G2_YMAX)
ax.set_yticks([])
style_ax(ax)

plt.tight_layout()
plt.savefig('figs/hbt_hist_dual.pdf', facecolor=navybg, edgecolor='none', dpi=300)
print("Saved figs/hbt_hist_dual.pdf")
plt.close()
