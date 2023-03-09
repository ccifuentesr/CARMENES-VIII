import numpy as np
import pandas as pd
import emcee
import corner
import radvel
import scipy.stats as ss
import os
import math
import matplotlib
from astropy.time import Time
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import matplotlib.gridspec as gridspec
from matplotlib.patches import ConnectionPatch
from pathlib import Path

fpath = Path(matplotlib.get_data_path(), "/Users/ccifuentesr/Library/Fonts/MinionPro-MediumCapt.otf")
plt.rcParams["font.family"] = "Georgia"
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.linewidth'] = 1.5

#=====================================
# Model and functions to run the MCMC
#=====================================

filename = 'RXJ1417'
# filename = 'RXJ1839'

"""
Parameters of the RV model:
---------------------------
- Vsys: systemic velocity (m/s)
- P: orbital period (d)
- K: RV semi-amplitude (m/s)
- t0: JD of conjuction (d)
- e: eccentricity
- w: argument of the periastron (rad)
- m: parameter of the linear trend
- q: parameter of the quadratic trend
-----------------------------
We use a parametrization with 1) secosw = np.sqrt(e)*np.cos(w), and 2) sesinw = np.sqrt(e)*np.sin(w) to avoid problems in the sampling since the priors of these new parameters can be gaussian centered in 0.
"""


def model_RV(Vsys, P, K, t0, secosw, sesinw, t):
    try:
        RV_array = np.zeros((len(P), len(t)))
    except:
        RV_array = np.zeros((1, len(t)))
    for i in range(RV_array.shape[0]):
        RV = Vsys[i]

        params = radvel.model.Parameters(num_planets = 1, basis = 'per tc secosw sesinw k')
        params['per1'].value = P[i]
        params['k1'].value = K[i]
        params['tc1'].value = t0[i]
        params['secosw1'].value = secosw[i]
        params['sesinw1'].value = sesinw[i]
        keplerian = radvel.model._standard_rv_calc(t, params, radvel.model.Vector(params))
        RV += keplerian

        RV_array[i, :] = RV
    return RV_array

def log_likelihood(theta, t, rv, erv):
    shape_theta = theta.shape
    if len(shape_theta) == 1:  # this case is for emcee. Bayev works with multiple dims
        theta = theta.reshape(1,-1)
        shape_theta = theta.shape
    log_like = np.zeros(shape_theta[0])
    for s in range(shape_theta[0]):
        Vsys, P, K, t0, secosw, sesinw, jitter = theta[s]

        model = model_RV([Vsys], [P], [K], [t0], [secosw], [sesinw], t)
        sigma2 = erv ** 2 + jitter ** 2
        log_like[s] = -0.5 * (len(t)*np.log(2*np.pi) + np.sum((rv - model) ** 2 / sigma2 + np.log(sigma2)))

    return log_like

def log_prior(theta, Priors, prior_type, param_names):
    shape_theta = theta.shape
    if len(shape_theta) == 1:    # this case is for emcee
        theta = theta.reshape(1,-1)
        shape_theta = theta.shape
    log_pr = np.zeros(shape_theta[0])
    for s in range(shape_theta[0]):
        for ind_p,p_name in enumerate(param_names):
            param = theta[s][ind_p]
            if prior_type[p_name] == 'u' and Priors[p_name][0] < param < Priors[p_name][1]:
                log_pr[s] += np.log(1.0/(Priors[p_name][1] - Priors[p_name][0]))
            elif prior_type[p_name] == 'g' and param > 0:
                log_pr[s] += np.log(1.0/(np.sqrt(2.0*np.pi)*Priors[p_name][1])) - 0.5*(param-Priors[p_name][0])**2/Priors[p_name][1]**2
            elif prior_type[p_name] == 'gt' and Priors[p_name][2] < param < Priors[p_name][3]:
                log_pr[s] += np.log(1.0/(np.sqrt(2.0*np.pi)*Priors[p_name][1])) - 0.5*(param-Priors[p_name][0])**2/Priors[p_name][1]**2
            else:
                log_pr[s] += -np.inf

    return log_pr

def log_probability(theta, t, rv, erv, Priors,  prior_type, param_names):
    lprior = log_prior(theta, Priors, prior_type, param_names)
    if not np.isfinite(lprior):
        return -np.inf, -np.inf

    return log_likelihood(theta, t, rv, erv) + lprior, lprior

#======================
#        MCMC
#======================

def fitMCMC(n_steps, mult_nw, t, rv, erv, Priors, prior_type):

    param_names = ['Vsys', 'P', 'K', 't0', 'secosw', 'sesinw', 'jitter']

    ndim  = len(param_names)
    nwalkers =  int(mult_nw * ndim)

    for p_name in param_names:
        if prior_type[p_name] == 'u':
            p0_n = [np.random.uniform(Priors[p_name][0], Priors[p_name][1], nwalkers)]
        elif prior_type[p_name] == 'g':
            p0_n = [np.random.normal(loc = Priors[p_name][0], scale = 0.2, size = nwalkers)]
        elif prior_type[p_name] == 'gt':
            param_val = [np.random.normal(loc = Priors[p_name][0], scale = 0.2, size = nwalkers)]
            #while np.any(np.abs(param_val) > 1):
            #    param_val = [np.random.normal(loc = Priors[p_name][0], scale = 0.2, size = nwalkers)]
            p0_n = param_val
        try:
            p0 = np.concatenate((p0, p0_n), axis = 0)
        except:
            p0 = p0_n
    p0 = p0.transpose()

    sampler = emcee.EnsembleSampler(nwalkers, ndim, log_probability, args = ([t, rv, erv, Priors,  prior_type, param_names]))
    state = sampler.run_mcmc(p0, nsteps = n_steps, progress = True)
    sampler.reset()
    sampler.run_mcmc(state.coords[np.argmax(state.log_prob)] + 1e-2 * np.random.randn(nwalkers, ndim), nsteps = int(n_steps/2), progress = True)

    flat_samples = sampler.get_chain(flat = True)

    return flat_samples, param_names

def plot_fitMCMC(t, rv, erv, flatsamples, param_names, flatsamples2 = None, param_names2 = None):

    Vsys, P, K, t0, secosw, sesinw, jitter = flatsamples[:, :7].T
    t_plot = np.linspace(min(t), min(t)+np.median(P), 1000)

    RV_fit = model_RV(Vsys, P, K, t0, secosw, sesinw, t_plot)

    fig, ax1 = plt.subplots(nrows = 1, ncols = 1, figsize = (12, 6))
    ax1.scatter(t, rv, c = 'k', s = 60)
    ax1.errorbar(t, rv, yerr = erv, c = 'k', linestyle = "none")

    muH1, sigmaH1 = RV_fit.mean(0), RV_fit.std(0)
    ax1.plot(t_plot, muH1, linewidth = 2, c = 'crimson')
    ax1.set_ylabel(r'$\Delta V_r$ [km s$^{-1}$]', fontsize = 20)
    ax1.set_xlabel(r'Time (BJD - 2457000)', fontsize = 20)
    #ax1.set_xticklabels([])
    ax1.fill_between(t_plot, muH1 - 2 * sigmaH1, muH1 + 2 * sigmaH1, alpha = 0.1, color = 'red')
    ax1.fill_between(t_plot, muH1 - sigmaH1, muH1 + sigmaH1, alpha = 0.2, color = 'red')

    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.tick_params('both', direction = 'in', length = 10, width = 1.5, which = 'major', labelsize = 15)
    ax1.tick_params('both', direction = 'in', length = 5, width = 0.5, which = 'minor')

    plt.savefig(filename + '.pdf', dpi = 900, bbox_inches = 'tight', pad_inches = 0.2)
    plt.show()

    # fig = corner.corner(flatsamples, labels = param_names)
    # plt.savefig(filename + '_cornerplot.pdf', dpi = 900, bbox_inches = 'tight', pad_inches = 0.2)
    # plt.show()

########

d = pd.read_csv('Data/'+filename+'.csv', sep = ',')
t = d.BJD.values #- 2457000
rv = d.RV.values
erv = d.eRV.values

prior_type = {'Vsys': 'u', 'P': 'g', 'K': 'gt', 't0': 'u', 'secosw': 'gt', 'sesinw': 'gt', 'jitter': 'u'}
# u -> uniform prior -> [from, to]
# g -> gaussian prior -> [mean, sd]
# gt -> gaussian truncated prior -> [mean, sd, min, max]

if filename == 'RXJ1417':
    e = 0.2023
    P = 464
    M_Msol = 0.475
    omega = np.radians(174.0907)
    sesinw_prior = np.sqrt(e)*np.sin(omega)
    secosw_prior = np.sqrt(e)*np.cos(omega)
    #
    Priors = {'Vsys':[-50, 0], 'P':[P, 10], 'K':[25, 5, 0, 50], 't0': [t[0], t[0] + 464], 'sesinw':[sesinw_prior, 0.01, -1, 1], 'secosw':[secosw_prior, 0.01, -1, 1], 'jitter':[0, 100]}

if filename == 'RXJ1839':
    e = 0.0
    P = 150
    M_Msol = 0.475
    omega = 0.0
    sesinw_prior = np.sqrt(e)*np.sin(omega)
    secosw_prior = np.sqrt(e)*np.cos(omega)
    #
    Priors = {'Vsys':[-50, 0], 'P':[P, 10], 'K':[25, 5, 0, 50], 't0': [t[0], t[0] + 464], 'sesinw':[sesinw_prior, 0.01, -1, 1], 'secosw':[secosw_prior, 0.01, -1, 1], 'jitter':[0, 100]}

# Fit and Corner plots
flatsamples_H1, paramnamesH1 = fitMCMC(int(2000), 4, t, rv, erv, Priors, prior_type)
for npar, p in zip(paramnamesH1, flatsamples_H1.mean(axis = 0)):
    print(npar, p)
plot_fitMCMC(t, rv, erv, flatsamples_H1, paramnamesH1)
