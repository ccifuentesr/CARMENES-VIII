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

input_file = 'cif03.v03'
df = pd.read_csv('Data/'+input_file+'.csv', sep=",", header=0)

BP_mag = df['phot_bp_mean_mag']
G_mag = df['phot_g_mean_mag']
RP_mag = df['phot_rp_mean_mag']
pi_mas = df['parallax']

def Mabs(mag, parallax):
    Mabs = mag - 5*np.log10(1000/parallax) + 5
    return Mabs

x = BP_mag - RP_mag
y = Mabs(G_mag, pi_mas)

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

xlabel = r'$G_{BP} - G_{RP}$ (mag)'
ylabel = r'$M_G$ (mag)'

fig, ax = plt.subplots(figsize=figsize)

#
ax.scatter(x, y, c='blue')

#
ax.tick_params(axis='x', labelsize=tickssize, direction='in',
                  top=True, labeltop=False, which='both', labelbottom=True)
ax.tick_params(axis='y', labelsize=tickssize, direction='in',
                  right=True, labelright=False, which='both')
ax.tick_params('both', direction = 'in', length = 10, width = 1.5, which = 'major', labelsize = labelsize)
ax.tick_params('both', direction = 'in', length = 5, width = 0.5, which = 'minor')
ax.xaxis.set_tick_params(which='minor', bottom=True, top=True)
ax.minorticks_on()
ax.set_xlabel(xlabel, size=labelsize)
ax.set_ylabel(ylabel, size=labelsize)
plt.gca().invert_yaxis()
# ax.set_xlim([400, 1000])
# ax.set_ylim([5, 500])
# ax.set_yscale('log')
#
plt.savefig('plot_MG.png', dpi=900, bbox_inches='tight')
plt.show()
