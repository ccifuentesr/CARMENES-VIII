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
plt.rcParams['axes.linewidth'] = 1.5

# =============================================================================
# DATA
# =============================================================================

input_file = 'cif03.v01'
output_file = input_file + '_out.csv'
df = pd.read_csv('Data/'+input_file+'.csv', sep=",", header=0)

ID_system = df['ID_system']

def param_muratio(pmra_1, pmdec_1, pmra_2, pmdec_2):
    muratio = np.sqrt(((pmra_1-pmra_2)**2 + (pmdec_1-pmdec_2)**2)/(pmra_1**2 + pmdec_1**2))
    return (muratio)

def pmtotal(pmra, pmdec, epmra, epmdec):
    pm_total = np.sqrt(pmra**2 + pmdec**2)
    epm_total = np.sqrt(epmra**2 + epmdec**2)
    return(pm_total, epm_total)

pmra_B, epmra_B = [], []
pmdec_B, epmdec_B = [], []
pmra_C, epmra_C = [], []
pmdec_C, epmdec_C = [], []
pmra_D, epmra_D = [], []
pmdec_D, epmdec_D = [], []

pmra_A_mas = df['pmra']
epmra_A_mas = df['pmra_error']
pmdec_A_mas = df['pmdec']
epmdec_A_mas = df['pmdec_error']

for i in range(len(df)-3):
    if 'A' in df['Component'][i]:
        if (ID_system[i] == ID_system[i+1]):
            pmra_B.append(df['pmra'][i+1])
            epmra_B.append(df['pmra_error'][i+1])
            pmdec_B.append(df['pmdec'][i+1])
            epmdec_B.append(df['pmdec_error'][i+1])
        else:
            pmra_B.append(np.nan)
            epmra_B.append(np.nan)
            pmdec_B.append(np.nan)
            epmdec_B.append(np.nan)
        if (ID_system[i] == ID_system[i+2]):
            pmra_C.append(df['pmra'][i+2])
            epmra_C.append(df['pmra_error'][i+2])
            pmdec_C.append(df['pmdec'][i+2])
            epmdec_C.append(df['pmdec_error'][i+2])
        else:
            pmra_C.append(np.nan)
            epmra_C.append(np.nan)
            pmdec_C.append(np.nan)
            epmdec_C.append(np.nan)
        if (ID_system[i] == ID_system[i+3]):
            pmra_D.append(df['pmra'][i+3])
            epmra_D.append(df['pmra_error'][i+3])
            pmdec_D.append(df['pmdec'][i+3])
            epmdec_D.append(df['pmdec_error'][i+3])
        else:
            pmra_D.append(np.nan)
            epmra_D.append(np.nan)
            pmdec_D.append(np.nan)
            epmdec_D.append(np.nan)
    else:
        pmra_B.append(np.nan)
        epmra_B.append(np.nan)
        pmdec_B.append(np.nan)
        epmdec_B.append(np.nan)
        pmra_C.append(np.nan)
        epmra_C.append(np.nan)
        pmdec_C.append(np.nan)
        epmdec_C.append(np.nan)
        pmra_D.append(np.nan)
        epmra_D.append(np.nan)
        pmdec_D.append(np.nan)
        epmdec_D.append(np.nan)

pmra_B_end = [np.nan, df['pmra'].iloc[-2], np.nan]
epmra_B_end = [np.nan, df['pmra_error'].iloc[-2], np.nan]
pmdec_B_end = [np.nan, df['pmdec'].iloc[-2], np.nan]
epmdec_B_end = [np.nan, df['pmdec_error'].iloc[-2], np.nan]
pmra_C_end = epmra_C_end = pmdec_C_end = epmdec_C_end = [np.nan, np.nan, np.nan]
pmra_D_end = epmra_D_end = pmdec_D_end = epmdec_D_end = [np.nan, np.nan, np.nan]

pmra_B_mas = pmra_B + pmra_B_end
epmra_B_mas = epmra_B + epmra_B_end
pmra_C_mas = pmra_C + pmra_C_end
epmra_C_mas = epmra_C + epmra_C_end
pmra_D_mas = pmra_D + pmra_D_end
epmra_D_mas = epmra_D + epmra_D_end
pmdec_B_mas = pmdec_B + pmdec_B_end
epmdec_B_mas = epmdec_B + epmdec_B_end
pmdec_C_mas = pmdec_C + pmdec_C_end
epmdec_C_mas = epmdec_C + epmdec_C_end
pmdec_D_mas = pmdec_D + pmdec_D_end
epmdec_D_mas = epmdec_D + epmdec_D_end

df_results = {'ID_star': df['ID_star'], \
'pmra_A_mas': pmra_A_mas, 'epmra_A_mas': epmra_A_mas, 'pmdec_A_mas': pmdec_A_mas, 'epmdec_A_mas': epmdec_A_mas,\
'pmra_B_mas': pmra_B_mas, 'epmra_B_mas': epmra_B_mas, 'pmdec_B_mas': pmdec_B_mas, 'epmdec_B_mas': epmdec_B_mas,\
'pmra_C_mas': pmra_C_mas, 'epmra_C_mas': epmra_C_mas, 'pmdec_C_mas': pmdec_C_mas, 'epmdec_C_mas': epmdec_C_mas,\
'pmra_D_mas': pmra_D_mas, 'epmra_D_mas': epmra_D_mas, 'pmdec_D_mas': pmdec_D_mas, 'epmdec_D_mas': epmdec_D_mas}

xp = np.linspace(0, 6000, 1000)

muratio_AB, muratio_AC, muratio_AD = [], [], []

for i in range(len(df)):
    try:
        muratio_AB.append(param_muratio(pmra_A_mas[i], pmdec_A_mas[i], pmra_B_mas[i], pmdec_B_mas[i]))
    except:
        muratio_AB.append(np.nan)
    try:
        muratio_AC.append(param_muratio(pmra_A_mas[i], pmdec_A_mas[i], pmra_C_mas[i], pmdec_C_mas[i]))
    except:
        muratio_AC.append(np.nan)
    try:
        muratio_AD.append(param_muratio(pmra_A_mas[i], pmdec_A_mas[i], pmra_D_mas[i], pmdec_D_mas[i]))
    except:
        muratio_AD.append(np.nan)

pmtotal_A, pmtotal_B, pmtotal_C, pmtotal_D = [], [], [], []

for i in range(len(df)):
    pmtotal_A.append(pmtotal(pmra_A_mas[i], pmdec_A_mas[i], epmra_A_mas[i], epmdec_A_mas[i])[0])
    pmtotal_B.append(pmtotal(pmra_B_mas[i], pmdec_B_mas[i], epmra_B_mas[i], epmdec_B_mas[i])[0])
    pmtotal_C.append(pmtotal(pmra_C_mas[i], pmdec_C_mas[i], epmra_C_mas[i], epmdec_C_mas[i])[0])
    pmtotal_D.append(pmtotal(pmra_D_mas[i], pmdec_D_mas[i], epmra_D_mas[i], epmdec_D_mas[i])[0])

pmA_out_AB = [pmtotal_A[i] for i in range(len(muratio_AB)) if muratio_AB[i] > 0.15]
pmB_out_AB = [pmtotal_B[i] for i in range(len(muratio_AB)) if muratio_AB[i] > 0.15]
pmA_out_AC = [pmtotal_A[i] for i in range(len(muratio_AC)) if muratio_AC[i] > 0.15]
pmC_out_AC = [pmtotal_C[i] for i in range(len(muratio_AC)) if muratio_AC[i] > 0.15]
pmA_out_AD = [pmtotal_A[i] for i in range(len(muratio_AD)) if muratio_AD[i] > 0.15]
pmD_out_AD = [pmtotal_D[i] for i in range(len(muratio_AD)) if muratio_AD[i] > 0.15]
#
pmA_in_AB = [pmtotal_A[i] for i in range(len(muratio_AB)) if muratio_AB[i] <= 0.15]
pmB_in_AB = [pmtotal_B[i] for i in range(len(muratio_AB)) if muratio_AB[i] <= 0.15]
pmA_in_AC = [pmtotal_A[i] for i in range(len(muratio_AC)) if muratio_AC[i] <= 0.15]
pmC_in_AC = [pmtotal_C[i] for i in range(len(muratio_AC)) if muratio_AC[i] <= 0.15]
pmA_in_AD = [pmtotal_A[i] for i in range(len(muratio_AD)) if muratio_AD[i] <= 0.15]
pmD_in_AD = [pmtotal_D[i] for i in range(len(muratio_AD)) if muratio_AD[i] <= 0.15]
#
OD_AB = [pmA_in_AB[i] - pmB_in_AB[i] for i in range(len(pmA_in_AB))]
OD_AC = [pmA_in_AC[i] - pmC_in_AC[i] for i in range(len(pmA_in_AC))]
OD_AD = [pmA_in_AD[i] - pmD_in_AD[i] for i in range(len(pmA_in_AD))]

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

xlabel = r'$\mu_{\rm A}$ (mas)'
ylabel = r'$\mu_{\rm B+}$ (mas)'

fig, ax = plt.subplots(2, 1, sharex='col',\
    gridspec_kw={'hspace': 0.1, 'wspace': 0.4, 'height_ratios': [10, 2], 'hspace': 0.03}, figsize=figsize)


#
ax[0].scatter(pmA_out_AB, pmB_out_AB, facecolors='None', edgecolors='r', s=pointsize, zorder=2)
ax[0].scatter(pmA_out_AC, pmC_out_AC, facecolors='None', edgecolors='r', s=pointsize, zorder=2)
ax[0].scatter(pmA_out_AD, pmD_out_AD, facecolors='None', edgecolors='r', s=pointsize, zorder=2)
#
ax[0].scatter(pmA_in_AB, pmB_in_AB, facecolors='None', edgecolors='k', s=pointsize, zorder=1)
ax[0].scatter(pmA_in_AC, pmC_in_AC, facecolors='None', edgecolors='k', s=pointsize, zorder=1)
ax[0].scatter(pmA_in_AD, pmD_in_AD, facecolors='None', edgecolors='k', s=pointsize, zorder=1)
#
ax[0].plot(xp, xp, '-', c='gainsboro', lw=2, zorder=0)
ax[0].plot(xp, xp*1.15, '--', c='gainsboro', lw=1.5, zorder=0)
ax[0].plot(xp, xp*0.85, '--', c='gainsboro', lw=1.5, zorder=0)
##
ax[1].scatter(pmA_in_AB, OD_AB, facecolors='none', edgecolors='k', s=pointsize, zorder=1)
ax[1].scatter(pmA_in_AC, OD_AC, facecolors='none', edgecolors='k', s=pointsize, zorder=1)
ax[1].scatter(pmA_in_AD, OD_AD, facecolors='none', edgecolors='k', s=pointsize, zorder=1)
#
ax[1].axhline(y=0, c='gainsboro', lw=2, ls='-', zorder=0)

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
ax[0].set_xlim([30, 5500])
ax[0].set_ylim([30, 5500])
ax[0].set_xscale('log')
ax[0].set_yscale('log')
#
ax[1].set_ylabel('O-C\n(pc)', size=labelsize*0.8)
ax[1].tick_params(axis='x', labelsize=tickssize, direction='in',
                  top=True, labeltop=False, which='both', labelbottom=False)
ax[1].tick_params(axis='y', labelsize=tickssize*0.8, direction='in',
                  right=True, labelright=False, which='both')
ax[1].tick_params('both', direction = 'in', length = 10, width = 1.5, which = 'major')
ax[1].tick_params('both', direction = 'in', length = 5, width = 0.5, which = 'minor')
ax[1].set_xlabel(xlabel, size=labelsize)
ax[1].set_xlim([30, 5500])
ax[1].set_ylim(-100, 100)

# =============================================================================
# OUT
# =============================================================================

plot_out = 'yes'
save_csv = 'no'
output_full = 'no'

if plot_out == 'yes':
    plt.savefig('Output/' + 'plot_pm_mas.png', dpi=900, bbox_inches='tight')

if save_csv == 'yes':
    df_append = pd.DataFrame(data=df_results)
    if output_full == 'yes':
        output = pd.concat([df, df_append], axis=1)
    else:
        output = df_append
    output.to_csv('Output/' + output_file, sep=',', encoding='utf-8')

plt.show()
