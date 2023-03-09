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

fpath = Path(matplotlib.get_data_path(), "/Users/ccifuentesr/Library/Fonts/MinionPro-MediumCapt.otf")
plt.rcParams["font.family"] = "Georgia"
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.linewidth'] = 1.5

# =============================================================================
# DATA
# =============================================================================

input_file = 'cif03.v01'
df = pd.read_csv('Data/'+input_file+'.csv', sep=",", header=0)

muratio = df['muratio']
deltaPA = df['deltaPA']
rho_arcsec = df['rho_all_arcsec']

muratio_in = [muratio[i] for i in range(len(df)) if muratio[i] < 0.15 and deltaPA[i] < 15]
deltaPA_in = [deltaPA[i] for i in range(len(df)) if muratio[i] < 0.15 and deltaPA[i] < 15]
muratio_in_out = [muratio[i] for i in range(len(df)) if muratio[i] < 0.25 and muratio[i] > 0.15 and deltaPA[i] < 15]
deltaPA_in_out = [deltaPA[i] for i in range(len(df)) if muratio[i] < 0.25 and muratio[i] > 0.15 and deltaPA[i] < 15]
muratio_out = [muratio[i] for i in range(len(df)) if muratio[i] > 0.25 and deltaPA[i] > 15]
deltaPA_out = [deltaPA[i] for i in range(len(df)) if muratio[i] > 0.25 and deltaPA[i] > 15]

x_in = muratio_in
y_in = deltaPA_in
x_in_out = muratio_in_out
y_in_out = deltaPA_in_out
x_out = muratio_out
y_out = deltaPA_out

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

xlabel = r'$\mu\,$' f'ratio'
ylabel = r'$\Delta PA$'

fig, ax = plt.subplots(figsize=figsize)

#
ax.scatter(x_in, y_in, facecolors='none', edgecolors='blue', s=pointsize, zorder=1)
ax.scatter(x_in_out, y_in_out, facecolors='none', edgecolors='orange', s=pointsize, zorder=1)
ax.scatter(x_out, y_out, facecolors='none', edgecolors='red', s=pointsize, zorder=1)
# ax.scatter(x, y, c='blue', s=pointsize, zorder=0)
ax.axhline(y=15, color='grey', linestyle='--', lw=linewidth, zorder=0)
ax.axvline(x=0.15, color='grey', linestyle='--', lw=linewidth, zorder=0)
ax.axvline(x=0.25, color='grey', linestyle='--', lw=linewidth, zorder=0)

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
# ax.set_xlim([400, 1000])
ax.set_ylim([1e-3, 1e2])
ax.set_xscale('log')
ax.set_yscale('log')

# =============================================================================
# SAVE
# =============================================================================

plt.savefig('Output/'+'plot_muratio_deltaPA.pdf', dpi=900, bbox_inches='tight')
plt.show()
