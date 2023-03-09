# %%

import numpy as np
import pandas as pd

version = '05'
input_name = 'cif03.v' + version
output_name = input_name + '_out.csv'

# Columns range

range_1 = np.arange(0,19)
range_2 = np.arange(19,24)
range_3 = np.arange(25,29)
range_4 = np.arange(29,40)
range_5 = np.arange(40,50)
range_6 = np.arange(50,70)
range_7 = np.arange(70,90)
range_8 = np.arange(90,112)

df_1 = pd.read_csv('Data/'+input_name+'.csv', nrows=3, usecols=range_1)
df_2 = pd.read_csv('Data/'+input_name+'.csv', nrows=3, usecols=range_2)
df_3 = pd.read_csv('Data/'+input_name+'.csv', nrows=3, usecols=range_3)
df_4 = pd.read_csv('Data/'+input_name+'.csv', nrows=3, usecols=range_4)
df_5 = pd.read_csv('Data/'+input_name+'.csv', nrows=3, usecols=range_5)
df_6 = pd.read_csv('Data/'+input_name+'.csv', nrows=3, usecols=range_6)
df_7 = pd.read_csv('Data/'+input_name+'.csv', nrows=3, usecols=range_7)
df_8 = pd.read_csv('Data/'+input_name+'.csv', nrows=3, usecols=range_8)

# %%

# dictionary = [[] for i in range(len(df))]

# for i in range(0, 2): 
#     for j in range(len(results['source_id'])):
#         dictionary[i].append({'Karmn': Karmn[i][j], 'Name': Name[i][j], 'source_id': source_id[i][j], 'ruwe': ruwe[i][j], 'dist':  dist[i][j]})
#         dictionary[i].append({k:[v] for k,v in dictionary[i][0].items()})
#         df_out = pd.DataFrame(dictionary[i])
#         # output = pd.concat([df, MR], axis=1)
#         df_out.to_csv(output_name, sep=',', encoding='utf-8')

# df_out = pd.DataFrame(df_1, df_2)
# df_out.to_csv(output_name, sep=',', encoding='utf-8')
# %%

df_test = pd.DataFrame({'Karmn': df_1['Karmn'][0], 'parallax': df_1['parallax'][0]}, index=['1', '2'])
# %%
