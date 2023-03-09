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
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import rc
from pathlib import Path
from scipy.optimize import curve_fit
from scipy.stats import ks_2samp

fpath = Path(matplotlib.get_data_path(), "/Users/ccifuentesr/Library/Fonts/MinionPro-MediumCapt.otf")
plt.rcParams["font.family"] = "Georgia"
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.linewidth'] = 1.5

# =============================================================================
# DATA
# =============================================================================

input_file = 'cif03.v03'
df = pd.read_csv('Data/'+input_file+'.csv', sep=",", header=0)

x = df['rho01']

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
cbarlabel = r'$q = \mathcal{M}_2/ \mathcal{M}_1$'

xlabel = r'$\rho$'f' [arcsec]'
ylabel = f'Number of pairs'

fig, ax = plt.subplots(figsize=figsize)

output_file = 'hist_rho'
plt.hist(x, bins=np.logspace(np.log10(1e-2), np.log10(1e5), 30), density=False,
alpha=1, histtype='step', color='blue', linewidth=linewidth)
ax.axvline(0.444, color='red', linestyle='dashed', linewidth=linewidth)

# ax.scatter(x1,y1)
# ax.scatter(x2,y2)
# ax.scatter(np.sort(x1), np.sort((func(x1, *popt1))), c='orange')
# ax.plot(x2, func(x2, *popt2), c='green')
# ax.semilogx(xfit1, yfit1, 'r-', lw=2)
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
ax.set_xlim([0.01, 100000])
# ax.set_ylim([5, 50])
ax.set_xscale('log')

# =============================================================================
# OUT
# =============================================================================

plt.savefig('Output/'+output_file+'.pdf', dpi=900, bbox_inches='tight')
plt.show()
