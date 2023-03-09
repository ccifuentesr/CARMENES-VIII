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
import matplotlib.patches as patches
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

n = 0
dt = 6 # 2016.0 to 2022.0
marcsec_deg = 86400*1000

figsize = (12, 10)
pointsize = 60
linewidth = 2
elinewidth = 2
tickssize = 22
labelsize = 22
legendsize = 18
cblabsize = 18

xlabel = r'$\alpha$ [deg]'
ylabel = r'$\delta$ [deg]'

fig, ax = plt.subplots(figsize=figsize)

for n in range(2):
    ra = df['ra'][n]
    dec = df['dec'][n]
    pmra = df['pmra'][n]
    pmdec = df['pmdec'][n]
    MG_mag = df['MG_mag'][n]
    #
    x, y, s = ra, dec, MG_mag*20
    dx, dy = pmra*dt/marcsec_deg, pmdec*dt/marcsec_deg # mas/a to deg
    #
    ax.scatter(x, y, c='r', s=s, zorder=0)
    plt.plot([x, dx], [y, dy], 'r-')
    # plt.annotate(xy=(dx, dy), xytext=(x, y), arrowprops=dict(arrowstyle='->'), text='')

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
frame = 0.01
ax.set_xlim([x-frame, x+frame])
ax.set_ylim([y-frame, y+frame])

# =============================================================================
# OUTPUT
# =============================================================================

filename = 'ra_dec'
# plt.savefig('Output/'+filename+'.pdf', dpi=900, bbox_inches='tight')
plt.show()
