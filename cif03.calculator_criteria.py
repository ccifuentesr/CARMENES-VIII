#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: ccifuentesr
"""

import numpy as np
import pandas as pd

# =============================================================================
# DATA
# =============================================================================

input_file = 'cif03.v01'
output_file = input_file + '_out.csv'
df = pd.read_csv('Data/'+input_file+'.csv', sep=",", header=0)

crit_Karmn = (df['Karmn'] != '')
crit_single = (df['Component'] == '-')


crit_1 = (df['ruwe'] >= 2.0)
crit_2 = (df['ipd_gof_harmonic_amplitude'] >= 0.1) & (df['ruwe'] > 1.4)
crit_3 = (df['rv_chisq_pvalue'] < 0.01) & (df['rv_renormalised_gof'] > 4) & (df['rv_nb_transits'] >= 10)
crit_4 = (df['duplicated_source'] == 1)
crit_5 = (df['radial_velocity_error'] > 8.0)

# =============================================================================
# WORK
# =============================================================================

# print(df['ruwe'][i] >= 2.0)

crit_ruwe, crit_ipd, crit_rv, crit_montes = [], [], [], []

for i in range(len(df)):
    crit_ruwe.append(df['ruwe'][i] >= 2.0)
    crit_ipd.append((df['ipd_gof_harmonic_amplitude'][i] >= 0.1) & (df['ruwe'][i] > 1.4))
    crit_rv.append((df['rv_chisq_pvalue'][i] < 0.01) & (df['rv_renormalised_gof'][i] > 4) & (df['rv_nb_transits'][i] >= 10))
    crit_montes.append((df['muratio'][i] <= 0.15) & (df['deltaPA'][i] < 15) & (df['deltad'][i] < 0.10))

df_results = {'ID_star': df['ID_star'], 'crit_ruwe': crit_ruwe, 'crit_ipd': crit_ipd,
'crit_rv': crit_rv, 'crit_montes': crit_montes}

# =============================================================================
# WRITE OUT
# =============================================================================

save_csv = 'yes'
output_full = 'no'

if save_csv == 'yes':
    df_append = pd.DataFrame(data=df_results)
    if output_full == 'yes':
        output = pd.concat([df, df_append], axis=1)
    else:
        output = df_append
    output.to_csv('Output/' + output_file, sep=',', encoding='utf-8')
