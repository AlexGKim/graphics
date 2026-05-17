#!/usr/bin/env python3
"""Generate left (|g^(1)|) and right (g^(2)) panels for sg_2.tex."""

import numpy as np
import matplotlib.pyplot as plt

navybg   = '#0d1b2a'
cyancol  = '#00dcff'
labelcol = '#dcdcdc'
axiscol  = '#b4b4b4'

tau_c = 2.0
tau   = np.linspace(0, 8, 1000)

g1    = np.exp(-(tau / tau_c) ** 2)          # |g^(1)(τ)|  Gaussian
g2    = 1 + np.exp(-(tau / tau_c) ** 2)      # g^(2)(τ) = 1 + |g^(1)|²


def style_ax(ax):
    ax.set_facecolor(navybg)
    ax.spines['bottom'].set_color(axiscol)
    ax.spines['left'].set_color(axiscol)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(colors=labelcol, labelsize=18)


fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(14, 4.5))
fig.subplots_adjust(left=0.07, right=0.97, bottom=0.15, top=0.95, wspace=0.7)
fig.patch.set_facecolor(navybg)

# ── Left panel: |g^(1)(τ)| ──────────────────────────────
ax_left.plot(tau, g1, color=cyancol, lw=2.5)
ax_left.axvline(tau_c, color=cyancol, lw=1.2, linestyle='--', alpha=0.7)
ax_left.set_xlabel(r'$\tau$', color=labelcol, fontsize=21)
ax_left.set_ylabel(r'$|g^{(1)}(\tau)|$', color=labelcol, fontsize=21)
ax_left.set_xlim(0, 8)
ax_left.set_ylim(-0.05, 1.15)
ax_left.set_yticks([0, 1])
ax_left.set_yticklabels(['0', '1'])
style_ax(ax_left)

# ── Right panel: g^(2)(τ) ───────────────────────────────
ax_right.fill_between(tau, 1, g2, color=cyancol, alpha=0.15)
ax_right.plot(tau, g2, color=cyancol, lw=2.5)
ax_right.axhline(1, color=axiscol, lw=1.2, linestyle='--', alpha=0.8)
ax_right.axvline(tau_c, color=cyancol, lw=1.2, linestyle='--', alpha=0.7)
ax_right.set_xlabel(r'$\tau$', color=labelcol, fontsize=21)
ax_right.set_ylabel(r'$g^{(2)}(\tau)$', color=labelcol, fontsize=21)
ax_right.set_xlim(0, 8)
ax_right.set_ylim(0, 2.3)
ax_right.set_yticks([1, 2])
ax_right.set_yticklabels(['1', '2'])
style_ax(ax_right)

plt.savefig('figs/sg2_panels.pdf', facecolor=navybg, edgecolor='none', dpi=300, bbox_inches='tight')
print("Saved figs/sg2_panels.pdf")
plt.close()
