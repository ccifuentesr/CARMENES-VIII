import numpy as np
import pandas as pd

# =============================================================================
# DATA
# =============================================================================

input_file = 'cif03.v02'
output_file = input_file + '_out.csv'
df = pd.read_csv('Data/'+input_file+'.csv', sep=",", header=0)

ID_system = df['ID_system']
# M1_Msol = df['M1_Msol']
# eM1_Msol = df['eM1_Msol']

# =============================================================================
# COMPUTE
# =============================================================================

Mass_A, eMass_A = [], []
Mass_B, eMass_B = [], []
Mass_total, eMass_total = [], []

empty = np.nan

for i in range(3, len(df)-3):
    # Component A
    if pd.isnull(df['System'][i]) == False:
        Mass_A.append(df['M_Msol'][i])
        eMass_A.append(df['eM_Msol'][i])
        Mass_B.append(empty)
        eMass_B.append(empty)
    # Component B
    elif (ID_system[i] == ID_system[i-1]) and pd.isnull(df['System'][i-1]) == False:
        Mass_B.append(df['M_Msol'][i])
        eMass_B.append(df['eM_Msol'][i])
        Mass_A.append(df['M_Msol'][i-1])
        eMass_A.append(df['eM_Msol'][i-1])
    # Component C
    elif (ID_system[i] == ID_system[i-2]) and pd.isnull(df['System'][i-2]) == False:
        Mass_B.append(df['M_Msol'][i])
        eMass_B.append(df['eM_Msol'][i])
        Mass_A.append(df['M_Msol'][i-2])
        eMass_A.append(df['eM_Msol'][i-2])
    else:
        Mass_A.append(empty)
        eMass_A.append(empty)
        Mass_B.append(empty)
        eMass_B.append(empty)


for i in range(3,len(df)-3):
    if (ID_system[i] == ID_system[i+1] == ID_system[i+2]): # A in Triple
        Mass_total.append(df['M_Msol'][i] + df['M_Msol'][i+1] + df['M_Msol'][i+2])
        eMass_total.append(np.sqrt(df['eM_Msol'][i]**2 + df['eM_Msol'][i+1]**2 + df['eM_Msol'][i+2]**2))
    elif (ID_system[i-1] == ID_system[i] == ID_system[i+1] ): # B in triple
        Mass_total.append(df['M_Msol'][i-1] + df['M_Msol'][i] + df['M_Msol'][i+1])
        eMass_total.append(np.sqrt(df['eM_Msol'][i-1]**2 + df['eM_Msol'][i]**2 + df['eM_Msol'][i+1]**2))
    elif (ID_system[i-2] == ID_system[i-1] == ID_system[i]): # C in triple
        Mass_total.append(df['M_Msol'][i-2] + df['M_Msol'][i-1] + df['M_Msol'][i])
        eMass_total.append(np.sqrt(df['eM_Msol'][i-2]**2 + df['eM_Msol'][i-1]**2 + df['eM_Msol'][i]**2))
    elif (ID_system[i] == ID_system[i+1] != ID_system[i+2] != ID_system[i-1]): # A in Double
        Mass_total.append(df['M_Msol'][i] + df['M_Msol'][i+1])
        eMass_total.append(np.sqrt(df['eM_Msol'][i]**2 + df['eM_Msol'][i+1]**2))
    elif (ID_system[i-1] == ID_system[i] != ID_system[i-2] != ID_system[i+1] != ID_system[i-2]): # B in double
        Mass_total.append(df['M_Msol'][i-1] + df['M_Msol'][i])
        eMass_total.append(df['eM_Msol'][i-1] + df['eM_Msol'][i])
    else:
        Mass_total.append(empty)
        eMass_total.append(empty)

ID_star = [df['ID_star'][i] for i in range(3, len(df)-3)]
print(len(ID_star))
df_results = {'ID_star': ID_star, 'Mass_A': Mass_A, 'eMass_A': eMass_A,
'Mass_B': Mass_B, 'eMass_B': eMass_B, 'Mass_tot': np.round(Mass_total, 5), 'eMass_tot': np.round(eMass_total, 5)}

# =============================================================================
# OUT
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
