#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: ccifuentesr
"""

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import uncertainties
import astropy
import math
from uncertainties.umath import *
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

# filter_OK = (df['Bool_MM'] == True)

MG_mag = df['MG_mag']
eMG_mag = df['eMG_mag']
M_Msol = df['M1_Msol']
eM_Msol = df['eM1_Msol']

# =============================================================================
# MAMAJEK TABLE
# =============================================================================

MG_mamajek = [2.99, 3.10, 3.26, 3.56, 3.66, 3.90, 4.105, 4.195, 4.325, 4.462,
4.635, 4.703, 4.757, 4.801, 4.914, 5.006, 5.098, 5.34, 5.553, 5.65, 5.83, 6.20,
6.53, 6.83, 7.02, 7.57, 7.74, 8.03]
Mass_mamajek = [1.44, 1.38, 1.33, 1.25, 1.21, 1.18, 1.13 ,1.08 ,1.06 ,1.03, 1.00,
0.99, 0.985, 0.98, 0.97, 0.95, 0.94, 0.90, 0.88, 0.86, 0.82, 0.78, 0.73, 0.70,
0.69, 0.64, 0.62, 0.59]
Radius_mamajek = [1.578, 1.533, 1.473, 1.359, 1.324, 1.221, 1.167, 1.142, 1.100,
1.060, 1.012, 1.002, 0.991, 0.977, 0.949, 0.927, 0.914, 0.853, 0.813, 0.797,
0.783, 0.755, 0.713, 0.701, 0.669, 0.630, 0.615, 0.608]
SpTnum_mamajek = [43, 44, 45, 46, 46, 47, 48, 49, 49.5, 50, 51, 52, 53, 54, 55,
56, 57, 58, 59, 0.07560, 61, 62, 63, 64, 65, 66, 67, 68, 69]

# =============================================================================
# FITTING
# =============================================================================

x = MG_mamajek
# y = Mass_mamajek
y = Radius_mamajek
#
k = 3
#
p, cov = np.polyfit(x, y, k, cov=True)
model = np.poly1d(p)
perr = np.sqrt(np.diag(cov))
#
xfit = np.sort(x)
yfit = np.polyval(p, xfit)

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

xlabel = r'$M_G$ 'f'(mag)'
# ylabel = r'$\mathcal{M} (\mathcal{M}_\odot)$'
ylabel = r'$\mathcal{R} (\mathcal{R}_\odot)$'

fig, ax = plt.subplots(figsize=figsize)

ax.scatter(x, y, facecolors='white', edgecolors='lightsteelblue', s=pointsize)
#
ax.plot(xfit, yfit, 'r-', lw=2)
#

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

# =============================================================================
# WRITE OUT
# =============================================================================

# output_file = 'plot_M_MG_mamajek'
output_file = 'plot_R_MG_mamajek'
save_csv = 'yes'
save_plot = 'yes'
output_full = 'no'

if save_csv == 'yes':
    MR_MG = np.round(model(df['MG_mag']), 4)
    #
    # df_results = {'ID_star': df['ID_star'], 'M_Msol': MR_MG}
    df_results = {'ID_star': df['ID_star'], 'R_Rsol': MR_MG}
    df_append = pd.DataFrame(data=df_results)
    if output_full == 'yes':
        output = pd.concat([df, df_append], axis=1)
    else:
        output = df_append
    output.to_csv('Output/' + input_file + '_out.csv', sep=',', encoding='utf-8')

if save_plot == 'yes':
    # plt.savefig('Output/'+output_file+'.pdf', dpi=900, bbox_inches='tight')
    plt.show()
