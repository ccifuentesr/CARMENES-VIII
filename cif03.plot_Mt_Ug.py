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

input_file = 'cif03.v03'
df = pd.read_csv('Data/'+input_file+'.csv', sep=",", header=0)

plot = 'Ug'
# plot = 's'

Ug = df['Ug_J']
eUg = df['eUg_J']
Porb_d = df['Porb_a']
ePorb_d = df['ePorb_a']
Mt_Msol = df['Mass_tot']
eMt_Msol = df['eMass_tot']
s01 = df['s01']

x = Mt_Msol

if plot == 'Ug':
    filename = 'plot_Mt_Ug.pdf'
    ylabel = r'$-U^\asterisk_G$'f' [J]'
    y = Ug
    z = np.log10(s01)*35

if plot == 's':
    filename = 'plot_Mt_s.pdf'
    ylabel = r'$s$ [au]'
    y = s01
    z = Ug

def s_Ga(Mtot, t):
    s_pc = 1.212*Mtot/t
    s_au = s_pc * 206265
    return s_au

xp = np.linspace(0, 3.5, 100)

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

xlabel = r'$\mathcal{M}_T$ [$\mathcal{M}_\odot$]'

fig, ax = plt.subplots(figsize=figsize)

#
if plot == 'Ug':
    ax.scatter(x[y > 1e34], y[y > 1e34], facecolors='none', edgecolors='blue', s=z[y > 1e34], zorder=0)
    ax.scatter(x[y < 1e34], y[y < 1e34], s=z[y < 1e34], facecolors='none', edgecolors='red', zorder=0)

if plot == 's':
    ax.scatter(x[z > 1e34], y[z > 1e34], facecolors='none', edgecolors='blue', s=pointsize, zorder=0)
    ax.scatter(x[z < 1e34], y[z < 1e34], s=pointsize, facecolors='none', edgecolors='red', zorder=0)
    ax.plot(xp, s_Ga(xp, 0.1), 'r--', lw=linewidth*2.5, zorder=0)
    ax.plot(xp, s_Ga(xp, 1), 'r--', lw=linewidth*1.5, zorder=0)
    ax.plot(xp, s_Ga(xp, 10), 'r--', lw=linewidth, zorder=0)
    ax.plot(xp, s_Ga(xp, 100), 'r--', lw=linewidth*0.5, zorder=0)

# =============================================================================
# CUSTOM
# =============================================================================

ax.tick_params(axis='x', labelsize=tickssize, direction='in',
                  top=True, labeltop=False, which='both', labelbottom=True)
ax.tick_params(axis='y', labelsize=tickssize, direction='in',
                  right=False, labelright=False, which='both')
ax.tick_params('both', direction = 'in', length = 10, width = 1.5, which = 'major')
ax.tick_params('both', direction = 'in', length = 5, width = 0.5, which = 'minor')
ax.xaxis.set_tick_params(which='minor', bottom=True, top=True)
ax.minorticks_on()
ax.set_xlabel(xlabel, size=labelsize)
ax.set_ylabel(ylabel, size=labelsize)
if plot == 'Ug':
    ax.set_xlim([0.01, 3.2])
    ax.set_ylim([1e32, 10e37])
    ax.set_yscale('log')
if plot == 's':
    ax.set_xlim([0.1, 3.2])
    ax.set_ylim([1, 230000])
    ax.set_yscale('log')


# =============================================================================
# SAVE
# =============================================================================

plt.savefig('Output/'+filename, dpi=900, bbox_inches='tight')
plt.show()
