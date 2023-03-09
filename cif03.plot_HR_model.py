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

filter_single = (df['Component'] == '-')
filter_multiple = (df['Component'] != '-')
filter_OK = (df['Bool_HR'] == True)
filter_KO = (df['Bool_HR'] == False)
filter_FGK = ((df['SpTnum'] >= 40) & (df['SpTnum'] <= 68))
#
BP_mag_single = df[filter_single & filter_OK]['BP_mag']
G_mag_single = df[filter_single & filter_OK]['G_mag']
RP_mag_single = df[filter_single & filter_OK]['RP_mag']
pi_mas_single = df[filter_single & filter_OK]['parallax']
#
BP_mag_multiple = df[filter_multiple & filter_OK]['BP_mag']
G_mag_multiple = df[filter_multiple & filter_OK]['G_mag']
RP_mag_multiple = df[filter_multiple & filter_OK]['RP_mag']
pi_mas_multiple = df[filter_multiple & filter_OK]['parallax']
#
BP_mag_multiple_FGK = df[filter_multiple & filter_OK & filter_FGK]['BP_mag']
G_mag_multiple_FGK = df[filter_multiple & filter_OK & filter_FGK]['G_mag']
RP_mag_multiple_FGK = df[filter_multiple & filter_OK & filter_FGK]['RP_mag']
pi_mas_multiple_FGK = df[filter_multiple & filter_OK & filter_FGK]['parallax']
#
BP_mag_wrong = df[filter_KO]['BP_mag']
G_mag_wrong = df[filter_KO]['G_mag']
RP_mag_wrong = df[filter_KO]['RP_mag']
pi_mas_wrong = df[filter_KO]['parallax']


def Mabs(mag, parallax):
    Mabs = mag - 5*np.log10(1000/parallax) + 5
    return Mabs

x_single = BP_mag_single - RP_mag_single
y_single = Mabs(G_mag_single, pi_mas_single)
x_multiple = BP_mag_multiple - RP_mag_multiple
y_multiple = Mabs(G_mag_multiple, pi_mas_multiple)
x_multiple_FGK = BP_mag_multiple_FGK - RP_mag_multiple_FGK
y_multiple_FGK = Mabs(G_mag_multiple_FGK, pi_mas_multiple_FGK)
x_wrong = BP_mag_wrong - RP_mag_wrong
y_wrong = Mabs(G_mag_wrong, pi_mas_wrong)

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
empty = '$\u25EF$'

xlabel = r'$G_{BP} - G_{RP}$ 'f'(mag)'
ylabel = r'$M_G$'f' (mag)'

fig, ax = plt.subplots(figsize=figsize)

#
ax.scatter(x_single, y_single, c='grey', marker=empty, s=pointsize, zorder=0)
ax.scatter(x_multiple, y_multiple, c='blue', s=pointsize, zorder=1)
ax.scatter(x_multiple_FGK, y_multiple_FGK, facecolors='none', edgecolors='orange', s=pointsize, zorder=1)
ax.scatter(x_wrong, y_wrong, marker='x', c='r', s=pointsize, zorder=1)

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
plt.gca().invert_yaxis()
# ax.set_xlim([400, 1000])
# ax.set_ylim([5, 500])
# ax.set_yscale('log')

# =============================================================================
# SAVE
# =============================================================================

plt.savefig('Output/'+'plot_MG.pdf', dpi=900, bbox_inches='tight')
plt.show()
