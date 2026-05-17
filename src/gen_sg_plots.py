#!/usr/bin/env python3
"""Generate g^(2) plot for sg_1.tex."""

import numpy as np
import matplotlib.pyplot as plt

# Color scheme from TikZ slides
navybg = '#0d1b2a'
source1col = '#00dcff'  # cyan (chaotic)
source2col = '#ffa500'  # orange (coherent)
fockcol = '#b464ff'     # purple (single-photon)
labelcol = '#dcdcdc'    # light grey
axiscol = '#b4b4b4'     # medium grey

# Figure setup
fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor(navybg)

# ════════════════════════════════════════════════════════
# g^(2)(τ) for three source types
# ════════════════════════════════════════════════════════
tau = np.linspace(0, 8, 1000)
tau_c = 2.0  # coherence time

# Chaotic/thermal light: g^(2)(τ) = 1 + exp(-(τ/τ_c)²)
g2_chaotic = 1 + np.exp(-(tau / tau_c)**2)

# Coherent (laser): g^(2)(τ) = 1 (constant)
g2_coherent = np.ones_like(tau)

# Single-photon (Fock): g^(2)(τ) = 1 - exp(-(τ/τ_c)²)
g2_fock = 1 - np.exp(-(tau / tau_c)**2)

ax.plot(tau, g2_chaotic, color=source1col, linewidth=3, label='Chaotic / thermal')
ax.plot(tau, g2_coherent, color=source2col, linewidth=3, label='Coherent (laser)')
ax.plot(tau, g2_fock, color=fockcol, linewidth=3, label='Single-photon (Fock)')


# Styling
ax.set_facecolor(navybg)
ax.set_xlabel(r'$\tau$', color=labelcol, fontsize=30)
ax.set_ylabel(r'$g^{(2)}(\tau)$', color=labelcol, fontsize=30)
ax.set_xlim(0, 8)
ax.set_ylim(-0.1, 2.2)

# Spine and tick styling
ax.spines['bottom'].set_color(axiscol)
ax.spines['left'].set_color(axiscol)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(colors=labelcol, labelsize=24)

# Grid
ax.grid(True, alpha=0.15, color=axiscol)

# Legend
ax.legend(loc='upper right', framealpha=0.92, facecolor=navybg, edgecolor=axiscol,
          labelcolor=labelcol, fontsize=24)

# y-axis ticks at key values
ax.set_yticks([0, 1, 2])
ax.set_yticklabels(['0', '1', '2'])

# Text labels to the left
ax.text(-0.8, 2, 'Bunching', color=labelcol, fontsize=20, ha='right', va='center')
ax.text(-0.8, 0, 'Antibunching', color=labelcol, fontsize=20, ha='right', va='center')

plt.tight_layout()
plt.savefig('figs/sg_g2_plot.pdf', facecolor=navybg, edgecolor='none', dpi=300)
print("Saved figs/sg_g2_plot.pdf")
plt.close()
