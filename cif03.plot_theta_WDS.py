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

filter_theta = df['Bool_rho'] == True

theta_WDS = df[filter_theta]['WDS_pa2']
theta_Gaia = df[filter_theta]['theta_deg']

x = theta_WDS
y = theta_Gaia

xp = np.linspace(0, 100, 1000)

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

xlabel = r'$\theta {\rm WDS}$ (arcsec)'
ylabel = r'$\theta {Gaia}$ (arcsec)'

fig, ax = plt.subplots(figsize=figsize)

#
ax.scatter(x, y, facecolors='none', edgecolors='k', s=pointsize, zorder=1)
#
ax.plot(xp, xp, '--', c='gainsboro', lw=2, zorder=0)
ax.plot(xp, xp*1.25, '--', c='gainsboro', lw=1.5, zorder=0)
ax.plot(xp, xp*0.75, '--', c='gainsboro', lw=1.5, zorder=0)


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
# ax.set_xlim([0.2, 6000])
# ax.set_ylim([0.2, 6000])
# ax.set_xscale('log')
# ax.set_yscale('log')
#
# plt.savefig('Output/'+'plot_theta_WDS.png', dpi=900, bbox_inches='tight')
plt.show()
