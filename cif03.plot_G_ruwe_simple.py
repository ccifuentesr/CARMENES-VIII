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

plt.rc('font', family='Helvetica')
rc('font', **{'family': 'Helvetica'})
plt.rcParams['mathtext.fontset'] = 'dejavusans'
plt.rcParams.update({'font.family':'Helvetica'})

# =============================================================================
# DATA
# =============================================================================

input_file = 'cif03.v01'
df = pd.read_csv('Data/'+input_file+'.csv', sep=",", header=0)

filter_single = df['Component'] == '-'
filter_multiple = df['Component'] != '-'

G_mag_single = df[filter_single]['phot_g_mean_mag']
G_mag_multiple = df[filter_multiple]['phot_g_mean_mag']
ruwe_single = df[filter_single]['ruwe']
ruwe_multiple = df[filter_multiple]['ruwe']

x_single = G_mag_single
y_single = ruwe_single
x_multiple = G_mag_multiple
y_multiple = ruwe_multiple

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
ylabel = r'ruwe'

fig, ax = plt.subplots(figsize=figsize)

#
ax.scatter(x_single, y_single, c='gainsboro', s=pointsize, zorder=0)
ax.scatter(x_multiple, y_multiple, c='blue', s=pointsize, zorder=1)
plt.axhline(y=1.4, color='red', linestyle='--', lw=2.5, zorder=2)
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
ax.set_ylim([0, 51])
# ax.set_yscale('log')
#
plt.savefig('Output/'+'plot_G_ruwe.png', dpi=900, bbox_inches='tight')
plt.show()
