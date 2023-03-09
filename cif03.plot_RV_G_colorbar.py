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
from mpl_toolkits.axes_grid1 import make_axes_locatable

plt.rc('font', family='Helvetica')
rc('font', **{'family': 'Helvetica'})
plt.rcParams['mathtext.fontset'] = 'dejavusans'
plt.rcParams.update({'font.family':'Helvetica'})

# =============================================================================
# DATA
# =============================================================================

input_file = 'cif03.v01'
df = pd.read_csv('Data/'+input_file+'.csv', sep=",", header=0)

RV = df['rv']
eRV = df['rv_error']
G_mag =  df['G_mag']
# eG_mag =  df['phot_g_mean_mag_error']
ruwe =  df['ruwe']

x = G_mag
y = eRV
ey = eRV
z = ruwe

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

xlabel = r'$G$ (mag)'
ylabel = r'$\sigma V_r$ (km s$^{-1}$)'
zlabel = r'ruwe'
cbarlabel = r'ruwe'
cmap = plt.get_cmap('copper_r')

fig, ax = plt.subplots(figsize=figsize)

#
sc = ax.scatter(x, y, c=z, s=pointsize, cmap=cmap, marker='o')
# ax.scatter(x, y, facecolors='none', edgecolors='blue', s=pointsize)
# ax.errorbar(x, y, yerr=ey, ms=10, fmt='o', color='lightgrey', markerfacecolor='red', ecolor='red', capthick=2, zorder=1)
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
# ax.set_xlim([0, 360])
ax.set_ylim([0.1, 100])
ax.set_yscale('log')
#

# Colorbar

divider = make_axes_locatable(plt.gca())
cax = divider.append_axes("right", "3%", pad="1%")
cbar = plt.colorbar(sc, cax=cax)  # Colorbar
cbar.set_label(cbarlabel, rotation=270, fontsize=labelsize, labelpad=30)
# sc.set_clim(vmin=-2, vmax=18)
# cbar.set_ticks(np.arange(-2, 19, 2))
# cbar.ax.set_yticklabels(SpT_half)
cbar.ax.tick_params(labelsize=cblabsize)
cbar.outline.set_visible(False)
#

plt.savefig('Output/'+'plot_rv_G.png', dpi=900, bbox_inches='tight')
plt.show()
