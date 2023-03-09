#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: ccifuentesr
"""

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import rc
from pathlib import Path
from scipy.optimize import curve_fit
from scipy.stats import ks_2samp

fpath = Path(matplotlib.get_data_path(), "/Users/ccifuentesr/Library/Fonts/MinionPro-MediumCapt.otf")
plt.rcParams["font.family"] = "Georgia"
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.linewidth'] = 1.5

# =============================================================================
# DATA
# =============================================================================

input_file = 'cif03.v03'
output_file = 'hist_cum_s'
df = pd.read_csv('Data/'+input_file+'.csv', sep=",", header=0)

def completeness_counter(s_au_count, s_au_lim, SpTnum, max_min, max_mass):
    """
    Returns the number of stars with a physical separation
    smaller than s_au_lim and restricted a maximum SpT.
    """
    N = len(df[(s_au_count <= s_au_lim) & (df['SpTnum'] < SpTnum) & (df['M_Msol'] > max_min) & (df['M_Msol'] < max_mass)]['s01'])
    return N

x00 = df[df['M_Msol'] >= 0.65]['s01']
y00 = [completeness_counter(x00, n, 80, 0, 10) for n in x00]
z00 = df[df['M_Msol'] >= 0.65]['q']

x01 = df[(df['M_Msol'] >= 0.25) & (df['M_Msol'] < 0.65)]['s01']
y01 = [completeness_counter(x01, n, 80, 0, 10) for n in x01]
z01 = df[(df['M_Msol'] >= 0.25) & (df['M_Msol'] < 0.65)]['q']

x02 = df[df['M_Msol'] < 0.25]['s01']
y02 = [completeness_counter(x02, n, 80, 0, 1) for n in x02]
z02 = df[df['M_Msol'] < 0.25]['q']

# =============================================================================
# FITTING
# =============================================================================

x1 = x00[(x00 > 5) & (x00 < 100)]
y1 = np.array(y00)[(x00 > 5) & (x00 < 100)]+20
x1_ = x00[(x00 > 100) & (x00 < 1000)]
y1_ = np.array(y00)[(x00 > 100) & (x00 < 1000)]
x1p = np.linspace(5,100,100)
#
x2 = x00[(x00 > 100) & (x00 < 1000)]
y2 = np.array(y00)[(x00 > 100) & (x00 < 1000)]+20
x2_ = x00[(x00 > 10) & (x00 < 100)]
y2_ = np.array(y00)[(x00 > 10) & (x00 < 100)]

def func(x, a, b):
    return (a + b * np.log(x))
#
popt1, pcov1 = curve_fit(func, x1, y1)
popt2, pcov2 = curve_fit(func, x2, y2)

print(10**(pcov1[1])) # Öpik exponent

# Kolmogorov-Smirnov test
# print(ks_2samp(x1, x2))

# =============================================================================
# PLOT
# =============================================================================

figsize = (10, 12)
pointsize = 60
linewidth = 2
elinewidth = 2
tickssize = 22
labelsize = 22
legendsize = 18
cblabsize = 18
empty = '$\u25EF$'

xlabel = r'$s$'f' [au]'
ylabel = f'Number of pairs'

fig = plt.figure(figsize=figsize)
gs = fig.add_gridspec(3, hspace=0)
ax = gs.subplots(sharex=True, sharey=False)

# Hide x labels and tick labels for all but bottom plot.
# for ax in axs:
#     ax.label_outer()

cmap = plt.get_cmap('gist_gray')
norm = matplotlib.colors.Normalize(vmin=0, vmax=1)

# Colormap
cmap = matplotlib.colors.ListedColormap(['grey', 'blue'])
bounds=[0, 0.5, 1]
norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

sc = ax[0].scatter(x00, y00, c='blue', s=pointsize*1.3, norm=norm, marker=empty)
sc = ax[1].scatter(x01, y01, c='blue', s=pointsize*1.3, norm=norm, marker=empty)
sc = ax[2].scatter(x02, y02, c='blue', s=pointsize*1.3, norm=norm, marker=empty)

ax[0].scatter(x00, y00, color='gainsboro', s=pointsize*1.2, marker=empty, zorder=0)
ax[1].scatter(x01, y01, color='gainsboro', s=pointsize*1.2, marker=empty, zorder=0)
ax[2].scatter(x02, y02, color='gainsboro', s=pointsize*1.2, marker=empty, zorder=0)

# Fitting for 01 only
# ax[0].plot(x1p, func(x1p, *popt1), c='magenta', lw=linewidth*1.4)
# ax[0].plot(x2, func(x2, *popt2), c='orange', lw=linewidth*1.4)

ax[0].axvline(100, color='grey', linestyle='dashed', linewidth=linewidth, zorder=0)
ax[0].axvline(2000, color='grey', linestyle='dashed', linewidth=linewidth, zorder=0)
ax[1].axvline(70, color='grey', linestyle='dashed', linewidth=linewidth, zorder=0)
ax[1].axvline(1000, color='grey', linestyle='dashed', linewidth=linewidth, zorder=0)
ax[2].axvline(40, color='grey', linestyle='dashed', linewidth=linewidth, zorder=0)
ax[2].axvline(300, color='grey', linestyle='dashed', linewidth=linewidth, zorder=0)

# plt.annotate(r'M', [10,10])
ax[0].annotate(r'$\mathcal{M}/\mathcal{M}_\odot \geq$ 0.65', xy=(0.05, 0.8), xycoords='axes fraction', size=22)
ax[1].annotate(r'0.25 < $\mathcal{M}/\mathcal{M}_\odot$ < 0.65', xy=(0.05, 0.8), xycoords='axes fraction', size=22)
ax[2].annotate(r'$\mathcal{M}/\mathcal{M}_\odot \leq$  0.25', xy=(0.05, 0.8), xycoords='axes fraction', size=22)

# =============================================================================
# CUSTOM
# =============================================================================

ax[0].tick_params(axis='x', labelsize=tickssize, direction='in',
                  top=True, labeltop=False, which='both', labelbottom=True)
ax[0].tick_params(axis='y', labelsize=tickssize, direction='in',
                  right=True, labelright=False, which='both')
ax[0].tick_params('both', direction = 'in', length = 10, width = 1.5, which = 'major')
ax[0].tick_params('both', direction = 'in', length = 5, width = 0.5, which = 'minor')
# ax.xaxis.set_tick_params(which='minor', bottom=True, top=True)
ax[0].minorticks_on()
ax[0].set_xlabel(xlabel, size=labelsize)
# ax[0].set_ylabel(ylabel, size=labelsize)
ax[0].set_xlim([0.05, 210000])
ax[0].set_ylim([0, 42])
ax[0].set_xscale('log')
#
ax[1].tick_params(axis='x', labelsize=tickssize, direction='in',
                  top=True, labeltop=False, which='both', labelbottom=True)
ax[1].tick_params(axis='y', labelsize=tickssize, direction='in',
                  right=True, labelright=False, which='both')
ax[1].tick_params('both', direction = 'in', length = 10, width = 1.5, which = 'major')
ax[1].tick_params('both', direction = 'in', length = 5, width = 0.5, which = 'minor')
ax[1].xaxis.set_tick_params(which='minor', bottom=True, top=True)
ax[1].minorticks_on()
ax[1].set_xlabel(xlabel, size=labelsize)
ax[1].set_ylabel(ylabel, size=labelsize)
ax[1].set_xlim([0.05, 210000])
ax[1].set_ylim([0, 500])
ax[1].set_xscale('log')
#
ax[2].tick_params(axis='x', labelsize=tickssize, direction='in',
                  top=True, labeltop=False, which='both', labelbottom=True)
ax[2].tick_params(axis='y', labelsize=tickssize, direction='in',
                  right=True, labelright=False, which='both')
ax[2].tick_params('both', direction = 'in', length = 10, width = 1.5, which = 'major')
ax[2].tick_params('both', direction = 'in', length = 5, width = 0.5, which = 'minor')
ax[2].xaxis.set_tick_params(which='minor', bottom=True, top=True)
ax[2].minorticks_on()
ax[2].set_xlabel(xlabel, size=labelsize)
# ax[2].set_ylabel(ylabel, size=labelsize)
ax[2].set_xlim([0.05, 210000])
ax[2].set_ylim([-.1, 220])
ax[2].set_xscale('log')

# divider = make_axes_locatable(plt.gca())
# cax = divider.append_axes("right", "2%", pad="1%")
# cbar = plt.colorbar(sc, cax=cax, boundaries=bounds, ticks=[0, 0.5, 1])  # Colorbar
# cbar.set_label(cbarlabel, rotation=270, fontsize=labelsize, labelpad=30)
sc.set_clim(vmin=0, vmax=1)
# cbar.ax.tick_params(labelsize=cblabsize)
# cbar.outline.set_visible(False)

# =============================================================================
# OUT
# =============================================================================

plt.savefig('Output/'+output_file+'.pdf', dpi=900, bbox_inches='tight')
plt.show()
