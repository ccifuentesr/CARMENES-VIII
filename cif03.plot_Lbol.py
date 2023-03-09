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

input_file = 'cif03.v02'
df = pd.read_csv('Data/'+input_file+'.csv', sep=",", header=0)

filter_single = (df['Component'] == '-')
filter_multiple = (df['Component'] != '-')

BP_mag_single = df[filter_single]['phot_bp_mean_mag']
G_mag_single = df[filter_single]['phot_g_mean_mag']
RP_mag_single = df[filter_single]['phot_rp_mean_mag']
J_mag_single = df[filter_single]['Jmag']
pi_mas_single = df[filter_single]['parallax']
L_Lsol_single = df[filter_single]['L_Lsol']
Teff_K_single = df[filter_single]['Teff_K']
#
BP_mag_multiple = df[filter_multiple]['phot_bp_mean_mag']
G_mag_multiple = df[filter_multiple]['phot_g_mean_mag']
RP_mag_multiple = df[filter_multiple]['phot_rp_mean_mag']
J_mag_multiple = df[filter_multiple]['Jmag']
pi_mas_multiple = df[filter_multiple]['parallax']
L_Lsol_multiple = df[filter_multiple]['L_Lsol']
Teff_K_multiple = df[filter_multiple]['Teff_K']
#
x_single = Teff_K_single
y_single = L_Lsol_single
x_multiple = Teff_K_multiple
y_multiple = L_Lsol_multiple

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

xlabel = r'$T_{\rm eff}$ (K)'
ylabel = r'$L_{\rm bol}$ ($L_\odot$)'

fig, ax = plt.subplots(figsize=figsize)

ax.scatter(x_single, y_single, facecolors='none', edgecolors='blue', s=pointsize, zorder=0)
ax.scatter(x_multiple, y_multiple, c='blue', s=pointsize, zorder=1)

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
# ax.set_xlim([400, 1000])
# ax.set_ylim([5, 500])
ax.set_yscale('log')
ax.invert_xaxis()

# =============================================================================
# OUTPUT
# =============================================================================

plt.savefig('Output/'+'plot_Lbol.png', dpi=900, bbox_inches='tight')
plt.show()
