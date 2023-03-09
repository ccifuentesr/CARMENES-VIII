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

input_file = 'cif03.v01'
df = pd.read_csv('Data/'+input_file+'.csv', sep=",", header=0)

filter_OK = (df['Bool_MM'] == True) # Single stars (avoiding unresolved binaries too)
filter_SpT = (df['SpTnum'] >= 70) & (df['SpTnum'] < 80)

type = 'M'
MG_max = 15

MG_mag = df[filter_OK]['MG_mag']
eMG_mag = df[filter_OK]['eMG_mag']
x, ex = MG_mag, eMG_mag
x_fit, ex_fit = MG_mag[MG_mag < MG_max], eMG_mag[MG_mag < MG_max]

if type == 'M':
    output_file = 'plot_M_MG'
    M_Msol = df[filter_OK]['M01']
    eM_Msol = df[filter_OK]['eM01']
    y, ey = M_Msol, eM_Msol
    y_fit, ey_fit = M_Msol[MG_mag < MG_max], eM_Msol[MG_mag < MG_max]
elif type == 'R':
    output_file = 'plot_R_MG'
    R_Rsol = df[filter_OK]['R01']
    eR_Rsol = df[filter_OK]['eR01']
    y, ey = R_Rsol, eR_Rsol
    y_fit, ey_fit = R_Rsol[MG_mag < MG_max], eR_Rsol[MG_mag < MG_max]

# =============================================================================
# FITTING
# =============================================================================

method = 'scipy'
# method = 'numpy'

if method == 'scipy':
    def func(x, a, b, c):
        return a*x**2 + b*x + c
    def func_err(x, ex, a, b, c, ea, eb, ec):
        return np.sqrt((x**2*ea)**2 + (x*eb)**2 + (ec)**2 + ((2*x*a + b)*ex)**2)
    #
    p, cov = scipy.optimize.curve_fit(func, x_fit, y_fit, sigma=ey_fit, absolute_sigma=True)
    ep = np.sqrt(np.diag(cov))
    #
    xp = np.linspace(min(x), MG_max, len(x))
    yp = func(xp, *p)
    #
    iter = 1000
    xp_rand = np.linspace(min(x), max(x), 100)
    #
    a_rand = np.random.normal(p[0], ep[0], iter)
    b_rand = np.random.normal(p[1], ep[1], iter)
    c_rand = np.random.normal(p[2], ep[2], iter)
    #
    OC = y - func(x, p[0], p[1], p[2])
    #
    for i in range(iter):
        y_model = func(xp, a_rand[i], b_rand[i], c_rand[i])
        if i == 0:
            y_model_array = y_model
        else:
            y_model_array = np.vstack((y_model_array, y_model))
    #
    y_model_mean = y_model_array.mean(0)
    y_model_std = y_model_array.std(0)
    #
    y_rand = [a_rand[i]*xp**2 + b_rand[i]*xp**1 + c_rand[i] for i in range(iter)]
    #
    stats = True
    #
    if stats == True:
        slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(func(x, *p), y)
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

if method == 'numpy':
    """DEPRECATED"""
    k = 2
    #
    p, cov = np.polyfit(x, y, k, cov=True)
    model = np.poly1d(p)
    perr = np.sqrt(np.diag(cov))
    #
    xfit = np.sort(x)
    yfit = np.polyval(p, xfit)
    #
    R2 = np.corrcoef(yfit, 10**model(xfit))[0, 1]**2
    #
    resid = yfit - model(xfit)
    #
    n, m = len(yfit), p.size
    dof = n - m
    #
    chi2 = np.sum((resid/model(xfit))**2)
    chi2red = chi2/(dof)
    s_err = np.sqrt(np.sum(resid**2)/(dof))
    #
    xp = np.linspace(min(x), max(x), 100)
    TT = np.vstack([xp**(k-i) for i in range(k+1)]).T
    yp = np.dot(TT, p)
    C_yp = np.dot(TT, np.dot(cov, TT.T))
    sig_yp = np.sqrt(np.diag(C_yp))
    #
    #
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(model(x), y)
    #
    stats = True

    if stats == True:
        print('Polynomial fitting:\n')
        print('degree =', k)
        print('coeffs =', p)
        print('err_coeffs =', perr)
        print('Pearsons r =', scipy.stats.pearsonr(model(x), y)[0])
        print('Spearmans rho =', scipy.stats.spearmanr(model(x), y)[0])
        print('Kendalls tau =', scipy.stats.kendalltau(model(x), y)[0])
        print('R2 score =', r2_score(y, model(x)))
        print('r_value =', r_value)
        print('p_value =', p_value)
        print('std_err =', std_err)
        print('R2 =', R2)
        print('chi2 =', chi2)
        print('chi2_red =', chi2red)

    OC = y - model(x)

print(p, ep)

# =============================================================================
# PLOT
# =============================================================================

plot, save_plot = True, True

if plot == True:
    figsize = (12, 10)
    pointsize = 60
    linewidth = 2
    elinewidth = 2
    tickssize = 22
    labelsize = 22
    legendsize = 18
    cblabsize = 18
    #
    xlabel = r'$M_G$ 'f'[mag]'
    if type == 'M':
        ylabel = r'$\mathcal{M}$ [$\mathcal{M}_\odot$]'
    elif type == 'R':
        ylabel = r'$\mathcal{R} [\mathcal{R}_\odot]$'

    fig, ax = plt.subplots(2, 1, sharex='col',\
        gridspec_kw={'hspace': 0.1, 'wspace': 0.4, 'height_ratios': [10, 2], 'hspace': 0.03}, figsize=figsize)

    ax[0].scatter(x, y, facecolors='white', edgecolors='lightsteelblue', s=pointsize)
    ax[0].errorbar(x, y, xerr=ex, yerr=ey, ls='none', ecolor='lightsteelblue', zorder=0)

    ax[0].plot(xp, yp, 'r-', lw=2)
    # for i in range(iter):
    #     ax[0].plot(xp_rand, y_rand[i], 'r-', alpha=.3, zorder=0)
    ax[0].fill_between(xp, y_model_mean - y_model_std, y_model_mean + y_model_std, color='r', alpha=.2, zorder=2)
    #
    ax[1].scatter(x, OC, facecolors='none', edgecolors='lightsteelblue', s=pointsize, zorder=1)
    ax[1].axhline(y=0, c='red', lw=2, ls='-', zorder=0)

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
    # ax[0].axes.xaxis.set_ticklabels([])
    #
    ax[1].tick_params(axis='x', labelsize=tickssize, direction='in',
                      top=True, labeltop=False, which='both', labelbottom=True)
    ax[1].tick_params(axis='y', labelsize=tickssize*0.8, direction='in',
                      right=True, labelright=False, which='both')
    ax[1].tick_params('both', direction = 'in', length = 10, width = 1.5, which = 'major')
    ax[1].tick_params('both', direction = 'in', length = 5, width = 0.5, which = 'minor')
    ax[1].set_xlabel(xlabel, size=labelsize)
    ax[1].set_ylabel(f'O-C 'r'[$\mathcal{M}_\odot]$', size=labelsize*0.8)
    ax[1].set_ylim(-.12, .12)
    #
    if save_plot == True:
        plt.savefig('Output/'+output_file+'.pdf', dpi=900, bbox_inches='tight')
        plt.show()

# =============================================================================
# WRITE OUT
# =============================================================================

save_csv, output_full = [True, False]

if save_csv == True:
    RM_MG = [np.round(func(df['MG_mag'][i], *p), 4) for i in range(len(df))]
    eRM_MG = [np.round(func_err(df['MG_mag'][i], df['eMG_mag'][i], *p, *ep), 4) for i in range(len(df))]
    #
    if type == 'M':
        df_results = {'ID_star': df['ID_star'], 'M_Msol': RM_MG, 'eM_Msol': eRM_MG}
    elif type == 'R':
        df_results = {'ID_star': df['ID_star'], 'R_Rsol': RM_MG, 'eR_Rsol': eRM_MG}
     #
    df_append = pd.DataFrame(data=df_results)
    if output_full == True:
        output = pd.concat([df, df_append], axis=1)
    else:
        output = df_append
    output.to_csv('Output/' + input_file + '_out.csv', sep=',', encoding='utf-8')
