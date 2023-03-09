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
from matplotlib import rc
from pathlib import Path
import math
from scipy.optimize import curve_fit

fpath = Path(matplotlib.get_data_path(), "/Users/ccifuentesr/Library/Fonts/MinionPro-MediumCapt.otf")
plt.rcParams["font.family"] = "Georgia"
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.linewidth'] = 1.5

# =============================================================================
# DATA
# =============================================================================

input_file = 'cif03.v01'
df = pd.read_csv('Data/'+input_file+'.csv', sep=",", header=0)

filter_single = (df['Component'] == '-')

def completeness_counter(d_pc_count, d_pc_lim, SpTnum):
    """
    Returns the number of stars with a distance smaller
    than d_pc_lim and restricted a maximum SpT.
    """
    N = len(df[(d_pc_count <= d_pc_lim) & ((df['SpTnum'] < SpTnum))]['d_pc'])
    return N

#
d_pc = df['d_pc']
ed_pc = df['ed_pc']

x = np.arange(min(d_pc), max(d_pc), .11)

alpha = .1
x_model = x
y_model = alpha*x**2

# x_log = np.logspace(np.log10(0.1), np.log10(100), 30)
# y_log = x_log

# =============================================================================
# PLOT
# =============================================================================

figsize = (12, 10)
pointsize = 60
linewidth = 2
elinewidth = 2
tickssize = 22
labelsize = 22
legendsize = 18
cblabsize = 18

xlabel = r'$d$ 'f'(pc)'
ylabel = f'Number of stars'

fig, ax = plt.subplots(figsize=figsize)
cmap = plt.cm.get_cmap('magma_r')
norm = matplotlib.colors.Normalize(vmin=-1, vmax=1)

for i in range(70,71,1):
    y = [completeness_counter(d_pc, n, i) for n in x]
    ax.plot(x, y, 'k-', linewidth=linewidth)
    # Fitting
    xp = x[(x > 10) & (x < 30)]
    yp = np.array(y)[(x > 10) & (x < 30)]
    def func(x, a, b):
        return (10**(a + b * np.log(x)))
    popt, pcov = curve_fit(func, xp, yp)
    ax.scatter(x, func(x, *popt), c=cmap(x), cmap='magma_r')
    ax.scatter(x, func(x, *popt), c=cmap(x), norm=norm, cmap='magma_r')


ax.axvline(30.42, color='red', linestyle='dashed', linewidth=linewidth)
# ax.axvline(35.32, color='red', linestyle='dashed', linewidth=linewidth)
# ax.axvline(35.97, color='red', linestyle='dashed', linewidth=linewidth)
# ax.axvline(33.88, color='red', linestyle='dashed', linewidth=linewidth)
# ax.axvline(32.06, color='red', linestyle='dashed', linewidth=linewidth)
# ax.axvline(24.01, color='red', linestyle='dashed', linewidth=linewidth)

# =============================================================================
# CUSTOM
# =============================================================================

ax.tick_params(axis='x', labelsize=tickssize, direction='in',
                  top=True, labeltop=False, which='both', labelbottom=True)
ax.tick_params(axis='y', labelsize=tickssize, direction='in',
                  right=True, labelright=False, which='both')
ax.tick_params('both', direction = 'in', length = 10, width = 1.5, which = 'major')
ax.tick_params('both', direction = 'in', length = 5, width = 0.5, which = 'minor')
ax.xaxis.set_tick_params(which='minor', bottom=True, top=True)
ax.minorticks_on()
ax.set_xlabel(xlabel, size=labelsize)
ax.set_ylabel(ylabel, size=labelsize)
# plt.gca().invert_yaxis()
ax.set_xlim([3, 40])
ax.set_ylim([3, 150])
ax.set_yscale('log')
ax.set_xscale('log')

# =============================================================================
# OUT
# =============================================================================

plt.savefig('Output/plot_d_completeness.pdf', dpi=900, bbox_inches='tight')
plt.show()
