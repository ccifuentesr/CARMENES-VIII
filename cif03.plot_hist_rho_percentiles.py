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
import scipy.stats
import sklearn
import RegscorePy as Reg
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error


fpath = Path(matplotlib.get_data_path(), "/Users/ccifuentesr/Library/Fonts/MinionPro-MediumCapt.otf")
plt.rcParams["font.family"] = "Georgia"
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.linewidth'] = 1.5

# =============================================================================
# DATA
# =============================================================================

input_file = 'cif03.v02'
df = pd.read_csv('Data/'+input_file+'.csv', sep=",", header=0)

def completeness_counter(s_au_count, s_au_lim, SpTnum, max_min, max_mass):
    """
    Returns the number of stars with a physical separation
    smaller than s_au_lim and restricted a maximum SpT.
    """
    N = len(df[(s_au_count <= s_au_lim) & (df['SpTnum'] < SpTnum) & (df['M_Msol'] > max_min) & (df['M_Msol'] < max_mass)]['s01'])
    return N

try:
    x00 = df[df['M_Msol'] < df['M_Msol'].quantile(q=1)]['s01']
    y00 = [completeness_counter(x00, n, 80, 0, 10) for n in x00]
    z00 = df[df['M_Msol'] < df['M_Msol'].quantile(q=1)]['q']
except:
    pass

cumulative = 'yes'
# cumulative = 'no'

# =============================================================================
# FITTING
# =============================================================================

x1 = x00[(x00 > 5) & (x00 < 85)]
y1 = np.array(y00)[(x00 > 5) & (x00 < 85)]
x1_ = x00[(x00 > 85) & (x00 < 1000)]
y1_ = np.array(y00)[(x00 > 85) & (x00 < 1000)]
x1p = np.linspace(5,85,100)
#
x2 = x00[(x00 > 85) & (x00 < 1000)]
y2 = np.array(y00)[(x00 > 85) & (x00 < 1000)]
x2_ = x00[(x00 > 10) & (x00 < 85)]
y2_ = np.array(y00)[(x00 > 10) & (x00 < 85)]
x2p = np.linspace(85,1000,100)

def func(x, a, b, l):
    return (a + b * np.log(x) ** (-l+1)) # General Öpik's law formulation
#
popt1, pcov1 = curve_fit(func, x1, y1)
popt2, pcov2 = curve_fit(func, x2, y2)
perr1 = np.sqrt(np.diag(pcov1))
perr2 = np.sqrt(np.diag(pcov2))
residuals1 = y1 - func(x1, *popt1)
residuals2 = y2 - func(x2, *popt2)

#chi_squared1 = np.sum(residuals1**2)
#chi_squared2 = np.sum(residuals2**2)
#dof1 = len(y1) - len(popt1)
#dof2 = len(y2) - len(popt2)
#reduced_chi_squared1 = chi_squared1 / dof1
#reduced_chi_squared2 = chi_squared2 / dof2
# chi_squared1 = np.sum((residuals1 / np.sqrt(np.abs(y1)))**2)
# chi_squared2 = np.sum((residuals2 / np.sqrt(np.abs(y2)))**2)
#print(popt1, perr1, reduced_chi_squared1) # Öpik exponent
#print(popt2, perr2, reduced_chi_squared2) # Öpik exponent

y1p_test = popt1[0] + popt1[1] * np.log(x1) ** (-popt1[2]+1) # Test = PREDICTION
y2p_test = popt2[0] + popt2[1] * np.log(x2) ** (-popt2[2]+1) # Test = PREDICTION

r2_1 = r2_score(y1, y1p_test)
r2_2 = r2_score(y2, y2p_test)
print("R-squared 1 =", r2_1)
print("R-squared 2 =", r2_2)

rmse_1 = np.sqrt(mean_squared_error(y1, y1p_test))
rmse_2 = np.sqrt(mean_squared_error(y2, y2p_test))
print("RMSE 1 =", rmse_1)
print("RMSE 2 =", rmse_2)
print("sd residuals 1 =", np.nanstd(residuals1))
print("sd residuals 2 =", np.nanstd(residuals2))


# y1p_test = -58.8 + 246.3 * np.log(x1p) ** (-0.3+1) # Miriam's PhD

# Kolmogorov-Smirnov test
# print(ks_2samp(x1, x2))

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

cbarlabel = r'$q = \mathcal{M}_2/ \mathcal{M}_1$'

xlabel = r'$s$'f' [au]'
ylabel = f'Number of pairs'

fig, ax = plt.subplots(figsize=figsize)
cmap = plt.get_cmap('gist_gray')
norm = matplotlib.colors.Normalize(vmin=0, vmax=1)

# make a color map of fixed colors
cmap = matplotlib.colors.ListedColormap(['grey', 'blue'])
bounds=[0, 0.5, 1]
norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

if cumulative == 'yes':
    output_file = 'hist_cum_s_single'
    sc = ax.scatter(x00, y00, c='blue', s=pointsize*1.3, norm=norm, marker=empty)
    ax.scatter(x00, y00, color='gainsboro', s=pointsize*1.2, marker=empty, zorder=0)
    ax.plot(x1p, func(x1p, *popt1), c='magenta', lw=linewidth*1.4)
    # ax.plot(x1p, y1p_test, c='magenta', lw=linewidth*1.4)
    ax.plot(x2p, func(x2p, *popt2), c='orange', lw=linewidth*1.4)
    #
    ax.axvline(85, color='grey', linestyle='dashed', linewidth=linewidth, zorder=0)
    ax.axvline(1000, color='grey', linestyle='dashed', linewidth=linewidth, zorder=0)

if cumulative == 'no':
    output_file = 'hist_rho'
    plt.hist(x, bins=np.logspace(np.log10(0.1), np.log10(13000), 25),
    density=False, alpha=1, histtype='step', color='blue', linewidth=linewidth,
    cumulative=0)
    ax.axvline(0.444, color='red', linestyle='dashed', linewidth=linewidth)

# =============================================================================
# CUSTOM
# =============================================================================

ax.tick_params(axis='x', labelsize=tickssize, direction='in',
                  top=True, labeltop=False, which='both', labelbottom=True)
ax.tick_params(axis='y', labelsize=tickssize, direction='in',
                  right=True, labelright=False, which='both')
ax.tick_params('both', direction = 'in', length = 10, width = 1.5, which = 'major')
ax.tick_params('both', direction = 'in', length = 5, width = 0.5, which = 'minor')
# ax.xaxis.set_tick_params(which='minor', bottom=True, top=True)
ax.minorticks_on()
ax.set_xlabel(xlabel, size=labelsize)
ax.set_ylabel(ylabel, size=labelsize)
ax.set_xlim([0.05, 210000])
# ax.set_ylim([5, 50])
ax.set_xscale('log')

# divider = make_axes_locatable(plt.gca())
# cax = divider.append_axes("right", "2%", pad="1%")
# cbar = plt.colorbar(sc, cax=cax, boundaries=bounds, ticks=[0, 0.5, 1])  # Colorbar
# cbar.set_label(cbarlabel, rotation=270, fontsize=labelsize, labelpad=30)
# sc.set_clim(vmin=0, vmax=1)
# cbar.ax.tick_params(labelsize=cblabsize)
# cbar.outline.set_visible(False)

# =============================================================================
# OUT
# =============================================================================

plt.savefig('Output/'+output_file+'.pdf', dpi=900, bbox_inches='tight')
plt.show()
