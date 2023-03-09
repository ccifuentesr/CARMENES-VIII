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

filter_single = df['Component'] == '-'
filter_multiple = df['Component'] != '-'


ra_single = df[filter_single]['ra']
RV_single = df[filter_single]['rv']
eRV_single = df[filter_single]['rv_error']
ra_multiple = df[filter_multiple]['ra']
RV_multiple = df[filter_multiple]['rv']
eRV_multiple = df[filter_multiple]['rv_error']

x_single = ra_single
y_single = RV_single
ey_single = eRV_single
x_multiple = ra_multiple
y_multiple = RV_multiple
ey_multiple = eRV_multiple

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

xlabel = r'$\alpha$ [deg]'
ylabel = r'$V_r$ [km s$^{-1}$]'

fig, ax = plt.subplots(figsize=figsize)

#
# ax.scatter(x_single, y_single, c='lightgrey', zorder=0)
# ax.scatter(x_multiple, y_multiple, c='red', zorder=1)
ax.errorbar(x_single, y_single, yerr=ey_single, ms=7, fmt='o', color='lightgrey', markerfacecolor='white', ecolor='lightgrey', capthick=2, zorder=0)
ax.errorbar(x_multiple, y_multiple, yerr=ey_multiple, ms=10, fmt='o', color='k', markerfacecolor='white', ecolor='k', capthick=2, zorder=1)
#
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
ax.set_xlim([0, 360])
# ax.set_ylim([5, 500])
# ax.set_yscale('log')
#
plt.savefig('Output/'+'plot_rv_ra.pdf', dpi=900, bbox_inches='tight')
plt.show()
