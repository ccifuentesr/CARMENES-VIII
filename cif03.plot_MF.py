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
df = pd.read_csv('Data/'+input_file+'.csv', sep=",", header=0)

d_pc =df['d_pc']

filter_Karmn = (pd.isnull(df['Karmn']) == False)
filter_primaries = (pd.isnull(df['System']) == False)
filter_single = ((df['Type'] == 'Single') | (df['Type'] == 'Single*'))
filter_multiple = ((df['Type'] == 'Multiple') | (df['Type'] == 'Multiple*'))
filter_double = ((df['Class'] == 'Double') | (df['Class'] == 'Double*'))
filter_triple = ((df['Class'] == 'Triple') | (df['Class'] == 'Triple*'))
filter_quadruple = ((df['Class'] == 'Quadruple') | (df['Class'] == 'Quadruple*'))
filter_quintuple = ((df['Class'] == 'Quintuple') | (df['Class'] == 'Quintuple*'))
filter_sextuple = ((df['Class'] == 'Sextuple') | (df['Class'] == 'Sextuple*'))

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
    return np.round(d_pc, 4)

def MF_CSF_SpT(df, SpTnum):
    """Use integer numbers for SpTnum (e.g. 70, 7, 72, etc.).
    """
    filter_SpT = ((df['SpTnum'] == SpTnum) | (df['SpTnum'] == SpTnum+0.5))
    filter_distance = (1000/df['parallax'] <= lim_d(SpTnum, 'limiting'))
    #
    N_all = len(df[filter_Karmn & filter_SpT]['ID_star'])
    N_single = len(df[filter_single & filter_Karmn & filter_SpT & filter_primaries & filter_distance]['ID_star'])
    N_double = len(df[filter_double & filter_Karmn & filter_SpT & filter_primaries & filter_distance]['ID_star'])
    N_triple = len(df[filter_triple & filter_Karmn & filter_SpT & filter_primaries & filter_distance]['ID_star'])
    N_quadruple = len(df[filter_quadruple & filter_Karmn & filter_SpT & filter_primaries & filter_distance]['ID_star'])
    N_quintuple = len(df[filter_quintuple & filter_Karmn & filter_SpT & filter_primaries & filter_distance]['ID_star'])
    N_sextuple = len(df[filter_sextuple & filter_Karmn & filter_SpT & filter_primaries & filter_distance]['ID_star'])
    MF = (N_double+N_triple+N_quadruple+N_quintuple+N_sextuple)/N_all*100
    CSF = (N_double+2*N_triple+3*N_quadruple+4*N_quintuple+5*N_sextuple)/N_all*100
    return(MF, CSF)

def MF_distance(df, distance, SpTnum):
    filter_SpT = ((df['SpTnum'] == SpTnum) | (df['SpTnum'] == SpTnum+0.5))
    MF_distance = len(df[filter_multiple & filter_Karmn & filter_SpT & (df['d_pc'] <= distance)]['ID_star'])
    return MF_distance

# =============================================================================
# STATISTICS
# =============================================================================

MF_SpT = [MF_CSF_SpT(df, n)[0] for n in np.arange(70, 79, 1)]
CSF_SpT = [MF_CSF_SpT(df, n)[1] for n in np.arange(70, 79, 1)]


# =============================================================================
# PLOT
# =============================================================================

plot = 'MF_SCF_SpT'

figsize = (12, 10)
pointsize = 60
linewidth = 2
elinewidth = 2
tickssize = 22
labelsize = 22
legendsize = 18
cblabsize = 18

fig, ax = plt.subplots(figsize=figsize)
cm = plt.cm.get_cmap('magma_r')
SpTypes = ['M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8']

if plot == 'MF_dist':
    output_file = 'plot_hist_MF'
    x = np.arange(min(d_pc), 30, 1)
    MF_d_pc = [MF_distance(df, n, 70) for n in x]
    MF_d_pc = [n/max(MF_d_pc) for n in MF_d_pc]
    y = MF_d_pc
    #
    xlabel = r'$d$'f'(pc)'
    ylabel = f'MF (%)'
    #
    ax.scatter(x, y, facecolors='none', edgecolors='orange', s=pointsize, hatch="/")
    #
    # ax.set_xscale('log')
    # ax.set_xlim([0,1])
    # ax.set_ylim([0,1])
elif plot == 'MF_SCF_SpT':
    output_file = 'plot_MF_SCF_SpT'
    xlabel = f'Spectral type'
    ylabel = f'MF and SCF (%)'
    x = np.arange(70, 79, 1)
    plt.bar(x-0.2, MF_SpT, width=0.4, bottom=None, align='center', fill = False, edgecolor = 'blue', linewidth=linewidth)
    plt.bar(x+0.2, CSF_SpT, width=0.4, bottom=None, align='center', fill = False, edgecolor = 'darkviolet', linewidth=linewidth, hatch="/")
    #
    plt.xticks(np.arange(70, 79, 1))
    ax.set_xticklabels(SpTypes)


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
# ax.set_xlim([0.05, 13000])
# ax.set_ylim([5, 50])

# =============================================================================
# OUT
# =============================================================================

plt.savefig('Output/'+output_file+'.pdf', dpi=900, bbox_inches='tight')
plt.show()
