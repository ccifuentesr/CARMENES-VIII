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

input_file = 'cif03.v03'
df = pd.read_csv('Data/'+input_file+'.csv', sep=",", header=0)

filter_single = (df['Component'] == '-')
filter_multiple = (df['Component'] != '-')
#
filter_WD = (df['HR_num'] == 1)
filter_WDc = (df['HR_num'] == 1.5)
filter_OBA = (df['HR_num'] == 2)
filter_FGK = (df['HR_num'] == 3)
filter_M = (df['HR_num'] == 4)
filter_LTY = (df['HR_num'] == 5)
filter_NMS = (df['HR_num'] == 6)
#
filter_KO = (df['HR_num'] == 0)
filter_OK = (df['Bool_HR'] == True)

# WD
BP_mag_multiple_WD = df[filter_multiple & filter_WD]['BP_mag']
G_mag_multiple_WD = df[filter_multiple & filter_WD]['G_mag']
RP_mag_multiple_WD = df[filter_multiple & filter_WD]['RP_mag']
pi_mas_multiple_WD = df[filter_multiple & filter_WD]['parallax']
BP_mag_multiple_WDc = df[filter_multiple & filter_WDc]['BP_mag']
G_mag_multiple_WDc = df[filter_multiple & filter_WDc]['G_mag']
RP_mag_multiple_WDc = df[filter_multiple & filter_WDc]['RP_mag']
pi_mas_multiple_WDc = df[filter_multiple & filter_WDc]['parallax']
# OBA
BP_mag_multiple_OBA = df[filter_multiple & filter_OBA]['BP_mag']
G_mag_multiple_OBA = df[filter_multiple & filter_OBA]['G_mag']
RP_mag_multiple_OBA = df[filter_multiple & filter_OBA]['RP_mag']
pi_mas_multiple_OBA = df[filter_multiple & filter_OBA]['parallax']
# FGK
BP_mag_multiple_FGK = df[filter_multiple & filter_FGK & filter_OK]['BP_mag']
G_mag_multiple_FGK = df[filter_multiple & filter_FGK & filter_OK]['G_mag']
RP_mag_multiple_FGK = df[filter_multiple & filter_FGK & filter_OK]['RP_mag']
pi_mas_multiple_FGK = df[filter_multiple & filter_FGK & filter_OK]['parallax']
# M
BP_mag_single_M = df[filter_single & filter_M]['BP_mag']
G_mag_single_M = df[filter_single & filter_M]['G_mag']
RP_mag_single_M = df[filter_single & filter_M]['RP_mag']
pi_mas_single_M = df[filter_single & filter_M]['parallax']
BP_mag_multiple_M = df[filter_multiple & filter_M & filter_OK]['BP_mag']
G_mag_multiple_M = df[filter_multiple & filter_M & filter_OK]['G_mag']
RP_mag_multiple_M = df[filter_multiple & filter_M & filter_OK]['RP_mag']
pi_mas_multiple_M = df[filter_multiple & filter_M & filter_OK]['parallax']
# LTY
BP_mag_multiple_LTY = df[filter_multiple & filter_LTY]['BP_mag']
G_mag_multiple_LTY = df[filter_multiple & filter_LTY]['G_mag']
RP_mag_multiple_LTY = df[filter_multiple & filter_LTY]['RP_mag']
pi_mas_multiple_LTY = df[filter_multiple & filter_LTY]['parallax']
# NMS
BP_mag_multiple_NMS = df[filter_multiple & filter_NMS & filter_OK]['BP_mag']
G_mag_multiple_NMS = df[filter_multiple & filter_NMS & filter_OK]['G_mag']
RP_mag_multiple_NMS = df[filter_multiple & filter_NMS & filter_OK]['RP_mag']
pi_mas_multiple_NMS = df[filter_multiple & filter_NMS & filter_OK]['parallax']
# KO
BP_mag_single_KO = df[filter_KO]['BP_mag']
G_mag_single_KO = df[filter_KO]['G_mag']
RP_mag_single_KO = df[filter_KO]['RP_mag']
pi_mas_single_KO = df[filter_KO]['parallax']

def Mabs(mag, parallax):
    Mabs = mag - 5*np.log10(1000/parallax) + 5
    return Mabs

x_multiple_WD = BP_mag_multiple_WD - RP_mag_multiple_WD
y_multiple_WD = Mabs(G_mag_multiple_WD, pi_mas_multiple_WD)
x_multiple_WDc = BP_mag_multiple_WDc - RP_mag_multiple_WDc
y_multiple_WDc = Mabs(G_mag_multiple_WDc, pi_mas_multiple_WDc)
#
x_multiple_OBA = BP_mag_multiple_OBA - RP_mag_multiple_OBA
y_multiple_OBA = Mabs(G_mag_multiple_OBA, pi_mas_multiple_OBA)
#
x_multiple_FGK = BP_mag_multiple_FGK - RP_mag_multiple_FGK
y_multiple_FGK = Mabs(G_mag_multiple_FGK, pi_mas_multiple_FGK)
#
x_single_M = BP_mag_single_M - RP_mag_single_M
y_single_M = Mabs(G_mag_single_M, pi_mas_single_M)
x_multiple_M = BP_mag_multiple_M - RP_mag_multiple_M
y_multiple_M = Mabs(G_mag_multiple_M, pi_mas_multiple_M)
#
x_multiple_LTY = BP_mag_multiple_LTY - RP_mag_multiple_LTY
y_multiple_LTY = Mabs(G_mag_multiple_LTY, pi_mas_multiple_LTY)
#
x_multiple_NMS = BP_mag_multiple_NMS - RP_mag_multiple_NMS
y_multiple_NMS = Mabs(G_mag_multiple_NMS, pi_mas_multiple_NMS)
#
x_single_KO = BP_mag_single_KO - RP_mag_single_KO
y_single_KO = Mabs(G_mag_single_KO, pi_mas_single_KO)

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

xlabel = r'$G_{BP} - G_{RP}$ 'f'[mag]'
ylabel = r'$M_G$'f' [mag]'

fig, ax = plt.subplots(figsize=figsize)
#
ax.scatter(x_single_M, y_single_M, c='lightsteelblue', marker=empty, s=pointsize, zorder=0)
ax.scatter(x_multiple_M, y_multiple_M, c='blue', s=pointsize, zorder=1)
ax.scatter(x_multiple_WD, y_multiple_WD, c='darkgrey', s=pointsize, zorder=1)
ax.scatter(x_multiple_WDc, y_multiple_WDc, c='grey',  marker=empty, s=pointsize, zorder=1)
ax.scatter(x_multiple_OBA, y_multiple_OBA, c='blueviolet', s=pointsize, zorder=1)
ax.scatter(x_multiple_FGK, y_multiple_FGK, c='orange', s=pointsize, zorder=1)
# ax.scatter(x_multiple_NMS, y_multiple_NMS, c='k', s=pointsize, zorder=1)
ax.scatter(x_single_KO, y_single_KO, c='r', marker='x', s=pointsize, zorder=1)
ax.scatter(x_multiple_LTY, y_multiple_LTY, c='k', s=pointsize, zorder=1)

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
plt.gca().invert_yaxis()
# ax.set_xlim([400, 1000])
# ax.set_ylim([5, 500])
# ax.set_yscale('log')

# =============================================================================
# SAVE
# =============================================================================

plt.savefig('Output/'+'plot_MG.pdf', dpi=900, bbox_inches='tight')
plt.show()
