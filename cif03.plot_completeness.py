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
from matplotlib.cbook import get_sample_data
import matplotlib.image as mpimg
from matplotlib import rc
import uncertainties
from astropy import constants as const

plt.rc('font', family='Helvetica')
rc('font', **{'family': 'Helvetica'})
plt.rcParams['mathtext.fontset'] = 'dejavusans'
plt.rcParams.update({'font.family':'Helvetica'})
plt.rcParams['axes.linewidth'] = 1.5

# =============================================================================
# DATA
# =============================================================================

data = 'Data/cif03.v01.csv'

df = pd.read_csv(data, sep=",", header=0)

filter_Karmn = df['Karmn'].notnull()

ID_star = df[filter_Karmn]['ID_star'].isnull()
SpT = df[filter_Karmn]['SpTnum']
d_pc = 1000/df[filter_Karmn]['parallax']

SpTnum = [70+i for i in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5,
        6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5]]
SpTypes = ['M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9']

# =============================================================================
# FUNCTIONS
# =============================================================================

def lim_d(SpT, type):
    """Limiting distance for a given spectral type.
    Limiting J-band magnitudes in Carmencita from Alonso-Floriano et al. 2015.
    Transformation between spectral type and MJ from Cifuentes et al. 2020.
    Choose type = 'limiting' or 'completeness'.

    Args:
        SpT (float): spectral type in numerical form (M0.0 V = 0.0, M0.5 V = 0.5, etc.)

    Returns:
        float: limiting distance in parsec.
    """
    SpT = SpT - 70 # Standard typing
    SpT_Jlim = {0.0: 8.5, 0.5: 8.5, 1.0: 9.0, 1.5: 9.0, 2.0: 9.5, 2.5: 9.5,
        3.0: 10.0, 3.5: 10.0, 4.0: 10.5, 4.5: 10.5, 5.0: 11.0, 5.5: 11.0,
        6.0: 11.5, 6.5: 11.5, 7.0: 11.5, 7.5: 11.5, 8.0: 11.5, 8.5: 11.5,
        9.0: 11.5, 9.5: 11.5}
    #
    SpT_Jcom = {0.0: 7.3, 0.5: 7.3, 1.0: 7.8, 1.5: 7.8, 2.0: 8.3, 2.5: 8.3,
        3.0: 8.8, 3.5: 8.8, 4.0: 9.3, 4.5: 9.3, 5.0: 9.8, 5.5: 9.8,
        6.0: 10.3, 6.5: 10.3, 7.0: 10.8, 7.5: 10.8, 8.0: 11.3, 8.5: 11.3,
        9.0: 11.3, 9.5: 11.3}
    #
    SpT_MJ = {0.0: 5.88, 0.5: 6.09, 1.0: 6.26, 1.5: 6.44, 2.0: 6.72, 2.5: 7.00,
        3.0: 7.35, 3.5: 7.67, 4.0: 7.97, 4.5: 8.41, 5.0: 9.08, 5.5: 9.48,
        6.0: 10.04, 6.5: 10.47, 7.0: 10.58, 7.5: 10.82, 8.0: 10.92, 8.5: 11.30,
        9.0: 11.51, 9.5: 11.68}
    #
    if type == 'limiting':
        m = SpT_Jlim[SpT]
    if type == 'completeness':
        m = SpT_Jcom[SpT]
    M = SpT_MJ[SpT]
    d_pc = 10**(((m-M)+5)/5)
    return d_pc

def xyr(SpT, type):
    xr = (SpT-0.25, SpT+0.25)
    yr = (lim_d(SpT, type), lim_d(SpT, type))
    return xr, yr

def counter(SpT_lim):
    filter = (SpT <= SpT_lim) & (d_pc <= lim_d(SpT_lim, 'limiting'))
    size = len(df[filter])
    return size

######
for n in np.arange(70, 80, 1):
    print(n, lim_d(n, 'limiting'), len(SpT[(df['SpTnum'] == n) | (df['SpTnum'] == n+0.5)]))

d_lim = [lim_d(n, 'limiting') for n in np.arange(70, 80, 1)]

x = SpT
y = d_pc

# counts = []
# print('SpTnum &  Size & Distance')
# for i in np.arange(0, 10, 0.5):
#     counts.append(counter(i))
#     print(i, ' & ', counter(i), ' & ', np.round(lim_d(i, 'limiting'), 2))

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
bins_size = np.arange(70.5, 82.5, 1)

fig, ax = plt.subplots(figsize=figsize)
# ax2 = ax.twinx()
cm = plt.cm.get_cmap('magma_r')

xlabel = r'Spectral type'
ylabel = r'$d$ (pc)'

ax.scatter(x, y, facecolors='none', edgecolors='k', s=pointsize, zorder=1)


for i in np.arange(0, 10, 1):
    ax.axhline(y=d_lim[i], xmin=i/10, xmax=i/10+0.1, color=cm((i+1)/10), linestyle='-', lw=linewidth*2) # i+1 avoids the light yellow

# plt.axhline(y=lim_d(71, 'limiting'), xmin=.1, xmax=10)#), xmin=70 , xmax=71 , color='r', linestyle='-', lw=4)

#
# n, bins, patches = plt.hist(SpTnum, bins=bins_size, color='red')
# bin_centers = 1 * (bins_size[:-1] + bins_size[1:])
#
# col = bin_centers - min(bin_centers)  # Scale values to interval [0,1]
# col = col/max(col)
# #
# for c, p in zip(col, patches):
#     plt.setp(p, 'facecolor', cm(c))

# =============================================================================
# CUSTOM
# =============================================================================

secondary_axes = 'no'

ax.tick_params(axis='x', labelsize=tickssize, direction='in',
                  top=True, labeltop=False, which='both', labelbottom=True)
ax.tick_params(axis='y', labelsize=tickssize, direction='in',
                  right=True, labelright=False, which='both')
ax.tick_params('both', direction = 'in', length = 10, width = 1.5, which = 'major')
ax.tick_params('both', direction = 'in', length = 5, width = 0.5, which = 'minor')
ax.xaxis.set_tick_params(which='minor', bottom=True, top=True)
# ax.minorticks_on()
ax.set_xlabel(xlabel, size=labelsize)
ax.set_ylabel(ylabel, size=labelsize)
ax.set_xlim([69.75, 79.75])
ax.set_ylim([0, 80])
plt.xticks(np.arange(70.0, 80.0, 0.5))
plt.setp(ax.xaxis.get_majorticklabels(), rotation=-45, ha="left")
ax.set_xticklabels(SpTypes)

if secondary_axes == 'yes':
    ax2.tick_params(axis='x', labelsize=tickssize, direction='in',
                      top=True, labeltop=False, which='both', labelbottom=True)
    ax2.tick_params(axis='y', labelsize=tickssize, direction='in',
                      right=True, labelright=True, which='both')
    ax2.tick_params('both', direction = 'in', length = 10, width = 1.5, which = 'major')
    ax2.tick_params('both', direction = 'in', length = 5, width = 0.5, which = 'minor')
    ax2.xaxis.set_tick_params(which='minor', bottom=True, top=True)
    ax2.minorticks_on()
    ax2.set_xlabel(xlabel, size=labelsize)
    ax2.set_ylabel('Number of stars', size=labelsize)
    ax2.yaxis.label.set_color('grey')
else:
    pass

# =============================================================================
# OUT
# =============================================================================

output_file = 'plot_SpT_d'
plt.savefig('Output/'+output_file+'.png', bbox_inches='tight')
plt.show()
