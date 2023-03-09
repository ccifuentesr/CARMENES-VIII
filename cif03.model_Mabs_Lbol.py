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
import math
import warnings
from uncertainties.umath import *
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.cbook import get_sample_data
import matplotlib.image as mpimg
from matplotlib import rc
import uncertainties
from astropy import constants as const
warnings.filterwarnings("ignore")

plt.rc('font', family='Helvetica')
rc('font', **{'family': 'Helvetica'})
plt.rcParams['mathtext.fontset'] = 'dejavusans'
plt.rcParams.update({'font.family':'Helvetica'})
plt.rcParams['axes.linewidth'] = 1.5

# =============================================================================
# DATA
# =============================================================================

data = 'cif03.v01'
output_file = data + '_out.csv'

df = pd.read_csv('Data/'+data + '.csv', sep=",", header=0)

J_mag = df['Jmag']
eJ_mag = df['eJmag']
parallax = df['parallax']
parallax_error = df['parallax_error']
G_mag = df['phot_g_mean_mag']
eG_mag = df['phot_g_mean_mag_error']

# =============================================================================
# FUNCTIONS
# =============================================================================

def Mabs_Lbol(J_mag, eJ_mag, parallax, parallax_error):
    J = uncertainties.ufloat(J_mag, eJ_mag)
    plx = uncertainties.ufloat(parallax, parallax_error)
    MJ = J - 5*log10(1000/plx) + 5
    if 4.4 <= MJ.n < 11.2:
        [a, b, c, d] = [uncertainties.ufloat(2.051, 0.075), uncertainties.ufloat(-0.662, 0.030), \
        uncertainties.ufloat(0.0267, 0.0039), uncertainties.ufloat(-0.00102, 0.00016)]
        Lbol = a + b*MJ + c*MJ**2 + d*MJ**3
        return(10**Lbol.n, 10**((Lbol.n-Lbol.s)))
    elif 11.2 <= MJ.n < 14.8:
        [a, b, c] = [uncertainties.ufloat(-3.906, 0.998), uncertainties.ufloat(0.334, 0.156), \
        uncertainties.ufloat(-0.0263, 0.0061)]
        Lbol = a + b*MJ + c*MJ**2
        return(10**Lbol.n, 10**((Lbol.n-Lbol.s)))
    else:
        return(np.nan, np.nan)

def MJ_SpT(J_mag, J_mag, parallax, parallax_error):
    J = uncertainties.ufloat(J_mag, eJ_mag)
    plx = uncertainties.ufloat(parallax, parallax_error)
    MJ = J - 5*log10(1000/plx) + 5
    Sptnum_SpT = [65, 67, 70.0, 70.5, 71.0, 71.5, 72.0 ,72.5, 73.0, 73.5, 74.0, 74.5, 75.0, 75.5, 76.0, 76.5, 77.0, 77.5, 78.0, 78.5, 79.0, 79.5]
    MJ_SpT = [5.13, 5.67, 5.87, 6.09, 6.26, 6.44, 6.72, 7.00, 7.35 , 7.67, 7.97, 8.41, 9.09, 9.48, 10.04, 10.47, 10.58, 10.82, 10.92, 11.30, 11.51, 11.68]
    Sptname = ['K5 V', 'K7 V', 'M0.0 V', 'M0.5 V', 'M1.0 V', 'M1.5 V', 'M2.0 V', 'M2.5 V', 'M3.0 V', 'M3.5 V', 'M4.0 V', 'M4.5 V', 'M5.0 V',\
     'M5.5 V', 'M6.0 V', 'M6.5 V', 'M7.0 V', 'M7.5 V', 'M8.0 V', 'M8.5 V', 'M9.0 V', 'M9.5 V']
    if MJ_SpT[0] - np.abs(MJ_SpT[0]-MJ_SpT[1])/2 < MJ.n <= MJ_SpT[0] + np.abs(MJ_SpT[0]-MJ_SpT[1])/2:
        return(Sptnum_SpT[0], Sptname[0])
    if MJ_SpT[-1] - np.abs(MJ_SpT[-1]-MJ_SpT[-2])/2 < MJ.n <= MJ_SpT[-1] + np.abs(MJ_SpT[-1]-MJ_SpT[-2])/2:
        return(Sptnum_SpT[-1], Sptname[-1])
    for i in range(1, len(MJ_SpT)-1):
        if MJ_SpT[i] - np.abs(MJ_SpT[i]-MJ_SpT[i-1])/2 < MJ.n <= MJ_SpT[i] + np.abs(MJ_SpT[i]-MJ_SpT[i+1])/2:
            return(Sptnum_SpT[i], Sptname[i])
    else:
        return(np.nan, np.nan)

def MG_SpT(G_mag, eG_mag, parallax, parallax_error):
    G = uncertainties.ufloat(G_mag, eG_mag)
    plx = uncertainties.ufloat(parallax, parallax_error)
    MG = G - 5*log10(1000/plx) + 5
    Sptnum_SpT = [65, 67, 70.0, 70.5, 71.0, 71.5, 72.0 ,72.5, 73.0, 73.5, 74.0, 74.5, 75.0, 75.5, 76.0, 76.5, 77.0, 77.5, 78.0, 78.5, 79.0, 79.5]
    MG_SpT = [6.82, 7.66, 8.01, 8.32, 8.61, 8.86, 9.24, 9.64, 10.08, 10.50, 10.87, 11.43, 12.22, 12.83, 13.62, 14.39, 14.47, 14.83, 14.98, 15.33, 16.08, 16.48]
    Sptname = ['K5 V', 'K7 V', 'M0.0 V', 'M0.5 V', 'M1.0 V', 'M1.5 V', 'M2.0 V', 'M2.5 V', 'M3.0 V', 'M3.5 V', 'M4.0 V', 'M4.5 V', 'M5.0 V',\
     'M5.5 V', 'M6.0 V', 'M6.5 V', 'M7.0 V', 'M7.5 V', 'M8.0 V', 'M8.5 V', 'M9.0 V', 'M9.5 V']
    if MG_SpT[0] - np.abs(MG_SpT[0]-MG_SpT[1])/2 < MG.n <= MG_SpT[0] + np.abs(MG_SpT[0]-MG_SpT[1])/2:
        return(MG_SpT[0], Sptname[0])
    if MG_SpT[-1] - np.abs(MG_SpT[-1]-MG_SpT[-2])/2 < MG.n <= MG_SpT[-1] + np.abs(MG_SpT[-1]-MG_SpT[-2])/2:
        return(Sptnum_SpT[-1], Sptname[-1])
    for i in range(1, len(MG_SpT)-1):
        if MG_SpT[i] - np.abs(MG_SpT[i]-MG_SpT[i-1])/2 < MG.n <= MG_SpT[i] + np.abs(MG_SpT[i]-MG_SpT[i+1])/2:
            return(Sptnum_SpT[i], Sptname[i])
    else:
        return(np.nan, np.nan)

# =============================================================================
# RESULTS
# =============================================================================

L_Lsol = [Mabs_Lbol(J_mag[i], eJ_mag[i], parallax[i], parallax_error[i])[0] for i in range(len(df))]
eL_Lsol = [Mabs_Lbol(J_mag[i], eJ_mag[i], parallax[i], parallax_error[i])[1] for i in range(len(df))]
SpTnum_J = [MJ_SpT(J_mag[i], eJ_mag[i], parallax[i], parallax_error[i])[0] for i in range(len(df))]
SpTnum_G = [MG_SpT(G_mag[i], eG_mag[i], parallax[i], parallax_error[i])[0] for i in range(len(df))]
SpT_J = [MJ_SpT(J_mag[i], eJ_mag[i], parallax[i], parallax_error[i])[1] for i in range(len(df))]
SpT_G = [MG_SpT(G_mag[i], eG_mag[i], parallax[i], parallax_error[i])[1] for i in range(len(df))]

print(SpT_G)

df_results = {'ID_star': df['ID_star'], 'L_Lsol': L_Lsol, 'eL_Lsol': eL_Lsol,\
    'SpTnum_J': SpTnum_J, 'SpTnum_G': SpTnum_G, 'SpT_J': SpT_J, 'SpT_G': SpT_G}

# =============================================================================
# WRITE OUT
# =============================================================================

save_csv = 'yes'
output_full = 'yes'

if save_csv == 'yes':
    df_append = pd.DataFrame(data=df_results)
    if output_full == 'yes':
        output = pd.concat([df, df_append], axis=1)
    else:
        output = df_append
    output.to_csv('Output/' + output_file, sep=',', encoding='utf-8')
