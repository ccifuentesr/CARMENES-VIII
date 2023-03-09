#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: ccifuentesr
"""

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import uncertainties
import astropy
import math
import scipy
from uncertainties.umath import *
from pathlib import Path
import scipy.stats
import sklearn
from sklearn.metrics import r2_score
import RegscorePy as Reg

fpath = Path(matplotlib.get_data_path(), "/Users/ccifuentesr/Library/Fonts/MinionPro-MediumCapt.otf")
plt.rcParams["font.family"] = "Georgia"
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.linewidth'] = 1.5

# =============================================================================
# DATA
# =============================================================================

input_file = 'vsini_fwhm'
df = pd.read_csv('Data/'+input_file+'.csv', sep=",", header=0)

vrot = df['vrot']
fwhm = df['fwhm']

x, y = vrot, fwhm

# =============================================================================
# FITTING
# =============================================================================

x_fit, y_fit = x[x > 2], y[x > 2]

def func(x, a, b, c, d, e):
    return a*x**4 + b*x**3 + c*x**2 + d*x + e
#
p, cov = scipy.optimize.curve_fit(func, x_fit, y_fit, absolute_sigma=True)
ep = np.sqrt(np.diag(cov))
#
xp = np.linspace(3, max(x), len(x))
yp = func(xp, *p)
#
iter = 1000
xp_rand = np.linspace(min(x), max(x), 100)
#
a_rand = np.random.normal(p[0], ep[0], iter)
b_rand = np.random.normal(p[1], ep[1], iter)
c_rand = np.random.normal(p[2], ep[2], iter)
d_rand = np.random.normal(p[3], ep[3], iter)
e_rand = np.random.normal(p[4], ep[4], iter)
#
OC = y - func(x, p[0], p[1], p[2], p[3], p[4])
#
for i in range(iter):
    y_model = func(xp, a_rand[i], b_rand[i], c_rand[i], d_rand[i], e_rand[i])
    if i == 0:
        y_model_array = y_model
    else:
        y_model_array = np.vstack((y_model_array, y_model))
#
y_model_mean = y_model_array.mean(0)
y_model_std = y_model_array.std(0)
#
y_rand = [a_rand[i]*xp**4 + b_rand[i]*xp**3 + c_rand[i]*xp**2 + d_rand[i]*x + e_rand[i] for i in range(iter)]
#
stats = True
slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(func(x, *p), y)
#
if stats == True:
    print('Polynomial fitting:\n')
    print('coeffs =', p)
    print('err_coeffs =', ep)
    print('Pearsons r =', scipy.stats.pearsonr(func(x, *p), y)[0])
    print('Spearmans rho =', scipy.stats.spearmanr(func(x, *p), y)[0])
    print('Kendalls tau =', scipy.stats.kendalltau(func(x, *p), y)[0])
    print('R2 score =', r2_score(y, func(x, *p)))
    print('r_value =', r_value)
    print('p_value =', p_value)
    print('std_err =', std_err)
#
def bic(y, p, n, k):
    """
    Calculates the Bayesian information criterion.
    BIC = n*log(residual sum of squares/n) + k*log(n)
    where:
    n: number of observations
    k: number of parameters (including intercept)
    y: true target variables
    p: polynomial fit (bic = parameters)
    """
    y_pred = func(x, p[0], p[1], p[2])
    res = np.sum(np.square(y - y_pred))
    bic = n*np.log(res/n) + k*np.log(n)
    return bic
# for i in range(1,5):
#     print(bic(y, p, len(x), k=i))

# =============================================================================
# PLOT
# =============================================================================

figsize = (12, 8)
pointsize = 60
linewidth = 2
elinewidth = 2
tickssize = 22
labelsize = 22
legendsize = 18
cblabsize = 18

xlabel = r'$v \sin{i}$ [km s$^{-1}$]'
ylabel = f'FWHM [$\AA$]'

fig, ax = plt.subplots(figsize=figsize)

ax.scatter(x, y, facecolors='white', edgecolors='k', s=pointsize)
ax.plot(xp, yp, 'r-', lw=2)
# ax.fill_between(xp, y_model_mean - y_model_std, y_model_mean + y_model_std, color='r', alpha=.2, zorder=2)

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
# ax[0].axes.xaxis.set_ticklabels([])

# =============================================================================
# WRITE OUT
# =============================================================================

output_file = 'plot_fwhm_vrot'

plt.savefig('Output/'+output_file+'.pdf', dpi=900, bbox_inches='tight')
plt.show()
