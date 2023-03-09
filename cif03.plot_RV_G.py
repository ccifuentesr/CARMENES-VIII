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
filter_crit_1 = (df['ruwe'] >= 2)
filter_crit_3 = ((df['rv_chisq_pvalue'] < 0.01) & (df['rv_renormalised_gof'] > 4) & (df['rv_nb_transits'] >= 10))

#
RV_single = df[filter_single]['rv']
eRV_single = df[filter_single]['rv_error']
G_mag_single = df[filter_single]['G_mag']
ruwe_single = df[filter_single]['ruwe']
#
RV_multiple = df[filter_multiple]['rv']
eRV_multiple = df[filter_multiple]['rv_error']
G_mag_multiple = df[filter_multiple]['G_mag']
ruwe_multiple = df[filter_multiple]['ruwe']
#
RV_single_crit_3 = df[filter_single & filter_crit_3]['rv']
eRV_single_crit_3 = df[filter_single & filter_crit_3]['rv_error']
G_mag_single_crit_3 = df[filter_single & filter_crit_3]['G_mag']
ruwe_single_crit_3 = df[filter_single & filter_crit_3]['ruwe']
#
RV_multiple_crit_3 = df[filter_multiple & filter_crit_3]['rv']
eRV_multiple_crit_3 = df[filter_multiple & filter_crit_3]['rv_error']
G_mag_multiple_crit_3 = df[filter_multiple & filter_crit_3]['G_mag']
ruwe_multiple_crit_3 = df[filter_multiple & filter_crit_3]['ruwe']


x_single = G_mag_single
y_single = eRV_single
z_single = ruwe_single
x_single_crit_3 = G_mag_single_crit_3
y_single_crit_3 = eRV_single_crit_3
z_single_crit_3 = ruwe_single_crit_3
x_multiple = G_mag_multiple
y_multiple = eRV_multiple
z_multiple = ruwe_multiple
x_multiple_crit_3 = G_mag_multiple_crit_3
y_multiple_crit_3 = eRV_multiple_crit_3
z_multiple_crit_3 = ruwe_multiple_crit_3

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

xlabel = r'$G$ 'f'[mag]'
ylabel = r'$\sigma V_r$ [km s$^{-1}$]'
zlabel = f'ruwe'

fig, ax = plt.subplots(figsize=figsize)

#
ax.scatter(x_multiple, y_multiple, facecolors='none', edgecolors='lightsteelblue', s=pointsize)
ax.scatter(x_single, y_single, facecolors='none', edgecolors='blue', s=pointsize)
ax.scatter(x_multiple_crit_3, y_multiple_crit_3, facecolors='none', edgecolors='orange', s=pointsize)
ax.scatter(x_single_crit_3, y_single_crit_3, facecolors='none', edgecolors='magenta', s=pointsize)
# ax.errorbar(x, y, yerr=ey, ms=10, fmt='o', color='lightgrey', markerfacecolor='red', ecolor='red', capthick=2, zorder=1)

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
# ax.set_xlim([0, 360])
ax.set_ylim([0.1, 100])
ax.set_yscale('log')

# =============================================================================
# OUTPUT
# =============================================================================

plt.savefig('Output/plot_G_rv.pdf', dpi=900, bbox_inches='tight')
plt.show()
