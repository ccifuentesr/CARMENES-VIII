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

input_file = 'cif03.v01'
output_file = input_file + '_out.csv'
df = pd.read_csv('Data/'+input_file+'.csv', sep=",", header=0)

ID_system = df['ID_system']

def ed_pc(d_pc, parallax, parallax_error):
    ed_pc = parallax_error/parallax * d_pc
    return ed_pc

d_B, ed_B = [], []
d_C, ed_C = [], []
d_D, ed_D = [], []

d_A_pc = 1000/df['parallax']
ed_A_pc = ed_pc(1000/df['parallax'], df['parallax'], df['parallax_error'])

for i in range(len(df)-3):
    if 'A' in df['Component'][i]:
        if (ID_system[i] == ID_system[i+1]):
            d_B.append(1000/df['parallax'][i+1])
            ed_B.append(ed_pc(1000/df['parallax'][i+1], df['parallax'][i+1], df['parallax_error'][i+1]))
        else:
            d_B.append(None)
            ed_B.append(None)
        if (ID_system[i] == ID_system[i+2]):
            d_C.append(1000/df['parallax'][i+2])
            ed_C.append(ed_pc(1000/df['parallax'][i+2], df['parallax'][i+2], df['parallax_error'][i+2]))
        else:
            d_C.append(None)
            ed_C.append(None)
        if (ID_system[i] == ID_system[i+3]):
            d_D.append(1000/df['parallax'][i+3])
            ed_D.append(ed_pc(1000/df['parallax'][i+3], df['parallax'][i+3], df['parallax_error'][i+3]))
        else:
            d_D.append(None)
            ed_D.append(None)
    else:
        d_B.append(None)
        ed_B.append(None)
        d_C.append(None)
        ed_C.append(None)
        d_D.append(None)
        ed_D.append(None)

d_B_end = [None, 1000/df['parallax'].iloc[-2], None]
ed_B_end = [None, ed_pc(1000/df['parallax'].iloc[-2], df['parallax'].iloc[-2], df['parallax_error'].iloc[-2]), None]
d_C_end = ed_C_end = d_D_end = ed_D_end = [None, None, None]

d_B_pc = d_B + d_B_end
ed_B_pc = ed_B + ed_B_end
d_C_pc = d_C + d_C_end
ed_C_pc = ed_C + ed_C_end
d_D_pc = d_D + d_D_end
ed_D_pc = ed_D + ed_D_end

df_results = {'ID_star': df['ID_star'], 'd_A_pc': d_A_pc,  'ed_A_pc': ed_A_pc, 'd_B_pc': d_B_pc, 'ed_B_pc': ed_B_pc,\
'd_C_pc': d_C_pc, 'ed_C_pc': ed_C_pc, 'd_D_pc': d_D_pc ,'ed_D_pc': ed_D_pc}

xp = np.linspace(0, 110, 100)
yp_up = [i*0.1 for i in xp]
yp_lo = [-i*0.1 for i in xp]

#
delta_dAB, delta_dAC, delta_dAD = [], [], []

for i in range(len(df)):
    try:
        delta_dAB.append(np.abs((d_A_pc[i]-d_B_pc[i])/d_A_pc[i]))
    except:
        delta_dAB.append(np.nan)
    try:
        delta_dAC.append(np.abs((d_A_pc[i]-d_C_pc[i])/d_A_pc[i]))
    except:
        delta_dAC.append(np.nan)
    try:
        delta_dAD.append(np.abs((d_A_pc[i]-d_D_pc[i])/d_A_pc[i]))
    except:
        delta_dAD.append(np.nan)

x_out_AB = [d_A_pc[i] for i in range(len(delta_dAB)) if delta_dAB[i] > 0.10]
y_out_AB = [d_B_pc[i] for i in range(len(delta_dAB)) if delta_dAB[i] > 0.10]
x_out_AC = [d_A_pc[i] for i in range(len(delta_dAC)) if delta_dAC[i] > 0.10]
y_out_AC = [d_C_pc[i] for i in range(len(delta_dAC)) if delta_dAC[i] > 0.10]
x_out_AB_err = [ed_A_pc[i] for i in range(len(delta_dAB)) if delta_dAB[i] > 0.10]
y_out_AB_err = [ed_B_pc[i] for i in range(len(delta_dAB)) if delta_dAB[i] > 0.10]
x_out_AC_err = [ed_A_pc[i] for i in range(len(delta_dAC)) if delta_dAC[i] > 0.10]
y_out_AC_err = [ed_C_pc[i] for i in range(len(delta_dAC)) if delta_dAC[i] > 0.10]

x_in_AB = [d_A_pc[i] for i in range(len(delta_dAB)) if delta_dAB[i] <= 0.10]
y_in_AB = [d_B_pc[i] for i in range(len(delta_dAB)) if delta_dAB[i] <= 0.10]
x_in_AC = [d_A_pc[i] for i in range(len(delta_dAC)) if delta_dAC[i] <= 0.10]
y_in_AC = [d_C_pc[i] for i in range(len(delta_dAC)) if delta_dAC[i] <= 0.10]
x_in_AD = [d_A_pc[i] for i in range(len(delta_dAD)) if delta_dAD[i] <= 0.10]
y_in_AD = [d_C_pc[i] for i in range(len(delta_dAD)) if delta_dAD[i] <= 0.10]
x_in_AB_err = [ed_A_pc[i] for i in range(len(delta_dAB)) if delta_dAB[i] <= 0.10]
y_in_AB_err = [ed_B_pc[i] for i in range(len(delta_dAB)) if delta_dAB[i] <= 0.10]
x_in_AC_err = [ed_A_pc[i] for i in range(len(delta_dAC)) if delta_dAC[i] <= 0.10]
y_in_AC_err = [ed_C_pc[i] for i in range(len(delta_dAC)) if delta_dAC[i] <= 0.10]
x_in_AD_err = [ed_A_pc[i] for i in range(len(delta_dAD)) if delta_dAD[i] <= 0.10]
y_in_AD_err = [ed_C_pc[i] for i in range(len(delta_dAD)) if delta_dAD[i] <= 0.10]

OD_in_AB = [x_in_AB[i] - y_in_AB[i] for i in range(len(x_in_AB))]
OD_in_AC = [x_in_AC[i] - y_in_AC[i] for i in range(len(x_in_AC))]
OD_in_AD = [x_in_AD[i] - y_in_AD[i] for i in range(len(x_in_AD))]
OD_out_AB = [x_out_AB[i] - y_out_AB[i] for i in range(len(x_out_AB))]
OD_out_AC = [x_out_AC[i] - y_out_AC[i] for i in range(len(x_out_AC))]

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

xlabel = r'$d_{\rm A}$'f' [pc]'
ylabel = r'$d_{\rm B+}$'f' [pc]'

# fig, ax = plt.subplots(figsize=figsize)
fig, ax = plt.subplots(2, 1, sharex='col',\
    gridspec_kw={'hspace': 0.1, 'wspace': 0.4, 'height_ratios': [10, 2], 'hspace': 0.03}, figsize=figsize)

#
ax[0].scatter(x_out_AB, y_out_AB, marker='x', color='r', s=pointsize, zorder=2)
ax[0].scatter(x_out_AC, y_out_AC, marker='x', color='r', s=pointsize, zorder=2)
#
ax[0].scatter(x_in_AB, y_in_AB, facecolors='none', edgecolors='b', s=pointsize, zorder=1)
ax[0].scatter(x_in_AC, y_in_AC, facecolors='none', edgecolors='b', s=pointsize, zorder=1)
ax[0].scatter(x_in_AD, y_in_AD, facecolors='none', edgecolors='b', s=pointsize, zorder=1)
#
ax[0].plot(xp, xp, '-', c='grey', lw=2, zorder=0)
ax[0].plot(xp, xp*1.10, '--', c='grey', lw=1.5, zorder=0)
ax[0].plot(xp, xp*0.90, '--', c='grey', lw=1.5, zorder=0)
##
ax[1].scatter(x_in_AB, OD_in_AB, facecolors='none', edgecolors='b', s=pointsize, zorder=1)
ax[1].scatter(x_in_AC, OD_in_AC, facecolors='none', edgecolors='b', s=pointsize, zorder=1)
ax[1].scatter(x_in_AD, OD_in_AD, facecolors='none', edgecolors='b', s=pointsize, zorder=1)
#
ax[1].scatter(x_out_AB, OD_out_AB, marker='x', color='r', s=pointsize, zorder=2)
ax[1].scatter(x_out_AC, OD_out_AC, marker='x', color='r', s=pointsize, zorder=2)
#
ax[1].axhline(y=0, c='grey', lw=2, ls='-', zorder=0)
ax[1].plot(xp, yp_up, c='grey', lw=2, ls='--', zorder=0)
ax[1].plot(xp, yp_lo, c='grey', lw=2, ls='--', zorder=0)

# =============================================================================
# CUSTOM
# =============================================================================

ax[0].tick_params(axis='x', labelsize=tickssize, direction='in',
                  top=True, labeltop=False, which='both', labelbottom=False)
ax[0].tick_params(axis='y', labelsize=tickssize, direction='in',
                  right=True, labelright=False, which='both')
ax[0].tick_params('both', direction = 'in', length = 10, width = 1.5, which = 'major')
ax[0].tick_params('both', direction = 'in', length = 5, width = 0.5, which = 'minor')
ax[0].xaxis.set_tick_params(which='minor', bottom=True, top=True)
ax[0].minorticks_on()
ax[0].set_xlabel('', size=labelsize)
ax[0].set_ylabel(ylabel, size=labelsize)
ax[0].axes.xaxis.set_ticklabels([])
# plt.gca().invert_yaxis()
ax[0].set_xlim([2, 100])
ax[0].set_ylim([2, 100])
ax[0].set_xscale('log')
ax[0].set_yscale('log')
#
ax[1].set_ylabel('O-C\n(pc)', size=labelsize*0.8)
ax[1].tick_params(axis='x', labelsize=tickssize, direction='in',
                  top=True, labeltop=False, which='both', labelbottom=True)
ax[1].tick_params(axis='y', labelsize=tickssize*0.8, direction='in',
                  right=True, labelright=False, which='both')
ax[1].tick_params('both', direction = 'in', length = 10, width = 1.5, which = 'major')
ax[1].tick_params('both', direction = 'in', length = 5, width = 0.5, which = 'minor')
ax[1].set_xlabel(xlabel, size=labelsize)
ax[1].set_xlim([2, 100])
ax[1].set_ylim(-5.5, 5.5)

# =============================================================================
# OUT
# =============================================================================

plot_out = 'yes'
save_csv = 'no'
output_full = 'no'

if plot_out == 'yes':
    plt.savefig('Output/' + 'plot_d_pc.pdf', dpi=900, bbox_inches='tight')

if save_csv == 'yes':
    df_append = pd.DataFrame(data=df_results)
    if output_full == 'yes':
        output = pd.concat([df, df_append], axis=1)
    else:
        output = df_append
    output.to_csv('Output/' + output_file, sep=',', encoding='utf-8')

plt.show()
