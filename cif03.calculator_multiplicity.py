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
import astropy
from astropy import stats

fpath = Path(matplotlib.get_data_path(), "/Users/ccifuentesr/Library/Fonts/MinionPro-MediumCapt.otf")
plt.rcParams["font.family"] = "Georgia"
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.linewidth'] = 1.5

# =============================================================================
# DATA AND FILTERS
# =============================================================================

input_file = 'cif03.v03'
df = pd.read_csv('Data/'+input_file+'.csv', sep=",", header=0)

SpTnum = [70+i for i in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5,
        6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5]]
SpTypes = ['M0.0--1.0\,V', 'M1.0--1.5\,V', 'M2.0--2.5\,V', 'M3.0--3.5\,V', 'M4.0--4.5\,V',
'M5.0--5.5\,V', 'M6.0--6.5\,V', 'M7.0--7.5\,V', 'M8.0--8.5\,V', 'M9.0--9.5\,V']


filter_karmn = (pd.isnull(df['Karmn']) == False) # Only Karmn stars
filter_primaries = (pd.isnull(df['System']) == False) # Only components 'A'
filter_candidate = (df['Type'] == 'Single*') # Only candidates to binaries from single
filter_candidate_bis = (df['Candidate'] == True) # Only candidates to binaries
#
filter_multiple = ((df['Type'] == 'Multiple') | (df['Type'] == 'Multiple*')) # Multiples
filter_single = ((df['Type'] == 'Single') | (df['Type'] == 'Single*')) # Singles
#
filter_double = ((df['Class'] == 'Double') | (df['Class'] == 'Double*'))
filter_triple = ((df['Class'] == 'Triple') | (df['Class'] == 'Triple*'))
filter_quadruple = ((df['Class'] == 'Quadruple') | (df['Class'] == 'Quadruple*'))
filter_quintuple = ((df['Class'] == 'Quintuple') | (df['Class'] == 'Quintuple*'))
filter_sextuple = ((df['Class'] == 'Sextuple') | (df['Class'] == 'Sextuple*'))
#
filter_double_cand = (df['Class'] == 'Single*')
filter_double_cand = (df['Class'] == 'Double*')
filter_triple_cand = (df['Class'] == 'Triple*')
filter_quadruple_cand = (df['Class'] == 'Quadruple*')
filter_quintuple_cand = (df['Class'] == 'Quintuple*')
filter_sextuple_cand = (df['Class'] == 'Sextuple*')
#
SpT = df[filter_karmn]['SpTnum']
d_pc = 1000/df[filter_karmn]['parallax']

# =============================================================================
# FUNCTIONS
# =============================================================================

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

def xyr(SpT, type):
    xr = (SpT-0.25, SpT+0.25)
    yr = (lim_d(SpT, type), lim_d(SpT, type))
    return xr, yr

def counter(SpT_lim):
    filter = (SpT <= SpT_lim) & (d_pc <= lim_d(SpT_lim, 'limiting'))
    size = len(df[filter])
    return size

######
if 1 == 0: # MF and CF for each SpT
    print('Spectral type & Sample size & MF [\%] & MF$^{\\ast}$ [\%] & CSF [\%] & [\%] & $q$ & \\\\')
    for n in np.arange(70, 80, 1):
        filter_SpT = ((df['SpTnum'] == n) | (df['SpTnum'] == n+0.5))
        filter_distance = (1000/df['parallax'] <= lim_d(n, 'limiting'))
        master_filter = filter_karmn & filter_primaries & filter_SpT & filter_distance
        #
        q = df[filter_karmn & filter_SpT]['q']
        s_au = df[filter_karmn & filter_SpT]['s01']
        #
        ALL = df[filter_karmn & filter_SpT]['Karmn']
        CAN = df[filter_karmn & filter_SpT & filter_candidate]['Karmn']
        PRI = df[master_filter]['Karmn']
        #
        MUL = df[master_filter & filter_multiple]['Karmn']
        SIN = df[master_filter & filter_single]['Karmn']
        #
        BIN = df[master_filter & filter_double]['Karmn']
        TRI = df[master_filter & filter_triple]['Karmn']
        QUA = df[master_filter & filter_quadruple]['Karmn']
        QUI = df[master_filter & filter_quintuple]['Karmn']
        SEX = df[master_filter & filter_sextuple]['Karmn']
        #
        BIN_cand = df[master_filter & filter_double_cand]['Karmn']
        TRI_cand = df[master_filter & filter_triple_cand]['Karmn']
        QUA_cand = df[master_filter & filter_quadruple_cand]['Karmn']
        QUI_cand = df[master_filter & filter_quintuple_cand]['Karmn']
        SEX_cand = df[master_filter & filter_sextuple_cand]['Karmn']
        #
        MF = len(MUL)/len(ALL)*100
        MF_EXT = (len(MUL) + len(CAN))/len(ALL)*100 # with candidates
        CSF = (len(BIN) + 2*len(TRI) + 3*len(QUA)+ 4*len(QUI) + 5*len(SEX))/len(ALL)*100
        # Note the next change in the definition: Double* == Triple
        CSF_cand = (len(CAN) + 2*len(BIN_cand) + 3*len(TRI_cand) + 4*len(QUA_cand)+ 5*len(QUI_cand) + 6*len(SEX_cand))/len(ALL)*100
        #
        # print(len(SEX))
        # BIN_F = len(BIN)/len(ALL)
        # TRI_F = len(TRI)/len(ALL)
        # QUA_F = len(QUA)/len(ALL)
        # QUI_F = len(QUI)/len(ALL)
        # SEX_F = len(SEX)/len(ALL)
        # systems = [BIN, TRI, QUA, QUI, SEX]
        #
        CI_95_MUL = astropy.stats.binom_conf_interval(k = len(MUL), n = len(ALL), confidence_level = 0.95, interval = 'wilson')*100
        CI_95_MUL_EXT = astropy.stats.binom_conf_interval(k = len(MUL) + len(CAN), n = len(ALL), confidence_level = 0.95, interval = 'wilson')*100
        CI_95_CSF = astropy.stats.binom_conf_interval(k = len(BIN) + 2*len(TRI) + 3*len(QUA)+ 4*len(QUI) + 5*len(SEX), n = len(ALL), confidence_level = 0.95, interval = 'wilson')*100
        CI_95_CSF_cand = astropy.stats.binom_conf_interval(k = len(CAN) + 2*len(BIN_cand) + 3*len(TRI_cand) + 4*len(QUA_cand)+ 5*len(QUI_cand) + 6*len(SEX_cand), n = len(ALL), confidence_level = 0.95, interval = 'wilson')*100
        #
        print(SpTypes[n-70], '&', len(SpT[(df['SpTnum'] == n) | (df['SpTnum'] == n+0.5)]), # lim_d(n, 'limiting'), '&'
        '&', np.round(MF, 1), '$^{+', np.round(CI_95_MUL[1] - MF, 1), '}_{-', np.round(MF - CI_95_MUL[0], 1), '}$',
        '&', np.round(MF_EXT, 1), '$^{+', np.round(CI_95_MUL_EXT[1] - MF_EXT, 1), '}_{-', np.round(MF_EXT - CI_95_MUL_EXT[0], 1), '}$',
        '&', np.round(CSF, 1), '$^{+', np.round(CI_95_CSF[1] - CSF, 1), '}_{-', np.round(CSF - CI_95_CSF[0], 1), '}$',
        '&', np.round(np.mean(q), 2), '\\\\ \\noalign{\\smallskip}	')

if 1 == 1: # MF and CF for all SpT or two ranges
    filter_SpT = ((df['SpTnum'] >= 75.5) & (df['SpTnum'] <= 79.5))
    filter_distance = (1000/df['parallax'] <= lim_d(75, 'limiting'))
    master_filter = filter_karmn & filter_primaries & filter_SpT
    #
    ALL = df[filter_karmn & filter_SpT]['Karmn']
    CAN = df[filter_karmn & filter_SpT & filter_candidate]['Karmn']
    PRI = df[master_filter]['Karmn']
    print(len(PRI))
    #
    MUL = df[master_filter & filter_multiple]['Karmn']
    SIN = df[master_filter & filter_single]['Karmn']
    #
    BIN = df[master_filter & filter_double]['Karmn']
    TRI = df[master_filter & filter_triple]['Karmn']
    QUA = df[master_filter & filter_quadruple]['Karmn']
    QUI = df[master_filter & filter_quintuple]['Karmn']
    SEX = df[master_filter & filter_sextuple]['Karmn']
    #
    BIN_cand = df[master_filter & filter_double_cand]['Karmn']
    TRI_cand = df[master_filter & filter_triple_cand]['Karmn']
    QUA_cand = df[master_filter & filter_quadruple_cand]['Karmn']
    QUI_cand = df[master_filter & filter_quintuple_cand]['Karmn']
    SEX_cand = df[master_filter & filter_sextuple_cand]['Karmn']
    #
    MF = len(MUL)/len(ALL)*100
    MF_EXT = (len(MUL) + len(CAN))/len(ALL)*100 # with candidates
    CSF = (len(BIN) + 2*len(TRI) + 3*len(QUA)+ 4*len(QUI) + 5*len(SEX))/len(ALL)*100
    #
    CI_95_MUL = astropy.stats.binom_conf_interval(k = len(MUL), n = len(ALL), confidence_level = 0.95, interval = 'wilson')*100
    CI_95_MUL_EXT = astropy.stats.binom_conf_interval(k = len(MUL) + len(CAN), n = len(ALL), confidence_level = 0.95, interval = 'wilson')*100
    CI_95_CSF = astropy.stats.binom_conf_interval(k = len(BIN) + 2*len(TRI) + 3*len(QUA)+ 4*len(QUI) + 5*len(SEX), n = len(ALL), confidence_level = 0.95, interval = 'wilson')*100
    #
    print(np.round(MF, 1), '$^{+', np.round(CI_95_MUL[1] - MF, 1), '}_{-', np.round(MF - CI_95_MUL[0], 1), '}$')
    print(np.round(MF_EXT, 1), '$^{+', np.round(CI_95_MUL_EXT[1] - MF_EXT, 1), '}_{-', np.round(MF_EXT - CI_95_MUL_EXT[0], 1), '}$')
    print(np.round(CSF, 1), '$^{+', np.round(CI_95_CSF[1] - CSF, 1), '}_{-', np.round(CSF - CI_95_CSF[0], 1), '}$')
