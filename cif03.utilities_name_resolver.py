import numpy as np
import pandas as pd
import astroquery
from astroquery.gaia import Gaia
from astroquery.simbad import Simbad
import re
import csv
astroquery.simbad.conf.server

# =============================================================================
# DATA
# =============================================================================

input_file = 'cif03.v04'
output_file = input_file + '_out.csv'
df = pd.read_csv('Data/'+input_file+'.csv', sep=",", header=0)

Name = df['Name_old']

# =============================================================================
# FUNCTION
# =============================================================================

def Simbad_name(object):
    """
    Gives the default identifier in Simbad for an object.
    """
    customSimbad = Simbad()
    customSimbad.add_votable_fields('sptype')
    result = customSimbad.query_object(object)
    return print(result['MAIN_ID'][0], result['SP_TYPE'][0])

def Simbad_name_string(name, string):
    """
    Checks if 'object' has the 'string' among its
    identificators in Simbad.
    Removes the unnecesary white spaces and leaves
    only the value and returns a string.
    """
    search = Simbad.query_objectids(name)
    for id in search:
        if string in str(id):
            return (re.sub(string+' ', '', re.sub(' +', ' ', id[0])))
        else:
            pass

# =============================================================================
# ACTION
# =============================================================================

GJ_name, G_name, HD_name, NAME_name, LP_name, V_name, Ross_name, Wolf_name, BD_name, LTT_name, RX_name, \
PM_name, PMJ_name, Gaia3_name, Gaia2_name, TMASS_name, WDS_name, Karmn_name, TMASS_id, WISE_id  = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

for i in range(len(df)):
    try:
        GJ_name.append(Simbad_name_string(Name[i], 'GJ'))
    except EOFError:
        GJ_name.append('')
    except TypeError:
        GJ_name.append('')
    except ConnectionError:
        GJ_name.append('')
    try:
        G_name.append(Simbad_name_string(Name[i], 'G '))
    except EOFError:
        G_name.append('')
    except TypeError:
        G_name.append('')
    except ConnectionError:
        G_name.append('')
    try:
        HD_name.append(Simbad_name_string(Name[i], 'HD'))
    except EOFError:
        HD_name.append('')
    except TypeError:
        HD_name.append('')
    except ConnectionError:
        HD_name.append('')
    try:
        NAME_name.append(Simbad_name_string(Name[i], 'NAME'))
    except EOFError:
        NAME_name.append('')
    except TypeError:
        NAME_name.append('')
    except ConnectionError:
        NAME_name.append('')
    try:
        LP_name.append(Simbad_name_string(Name[i], 'LP '))
    except EOFError:
        LP_name.append('')
    except TypeError:
        LP_name.append('')
    except ConnectionError:
        LP_name.append('')
    try:
        V_name.append(Simbad_name_string(Name[i], 'V*'))
    except EOFError:
        V_name.append('')
    except TypeError:
        V_name.append('')
    except ConnectionError:
        V_name.append('')
    try:
        Wolf_name.append(Simbad_name_string(Name[i], 'Wolf'))
    except EOFError:
        Wolf_name.append('')
    except TypeError:
        Wolf_name.append('')
    except ConnectionError:
        Wolf_name.append('')
    try:
        Ross_name.append(Simbad_name_string(Name[i], 'Ross'))
    except EOFError:
        Ross_name.append('')
    except TypeError:
        Ross_name.append('')
    except ConnectionError:
        Ross_name.append('')
    try:
        BD_name.append(Simbad_name_string(Name[i], 'BD'))
    except EOFError:
        BD_name.append('')
    except TypeError:
        BD_name.append('')
    except ConnectionError:
        BD_name.append('')
    try:
        LTT_name.append(Simbad_name_string(Name[i], 'LTT'))
    except EOFError:
        LTT_name.append('')
    except TypeError:
        LTT_name.append('')
    except ConnectionError:
        LTT_name.append('')
    try:
        RX_name.append(Simbad_name_string(Name[i], 'RX'))
    except EOFError:
        RX_name.append('')
    except TypeError:
        RX_name.append('')
    except ConnectionError:
        RX_name.append('')
    try:
        PM_name.append(Simbad_name_string(Name[i], 'PM '))
    except EOFError:
        PM_name.append('')
    except TypeError:
        PM_name.append('')
    except ConnectionError:
        PM_name.append('')
    try:
        PMJ_name.append(Simbad_name_string(Name[i], 'PM J'))
    except EOFError:
        PMJ_name.append('')
    except TypeError:
        PMJ_name.append('')
    except ConnectionError:
        PMJ_name.append('')
    try:
        Gaia2_name.append(Simbad_name_string(Name[i], 'Gaia DR2'))
    except EOFError:
        Gaia2_name.append('')
    except TypeError:
        Gaia2_name.append('')
    except ConnectionError:
        Gaia2_name.append('')
    try:
        Gaia3_name.append(Simbad_name_string(Name[i], 'Gaia EDR3'))
    except EOFError:
        Gaia3_name.append('')
    except TypeError:
        Gaia3_name.append('')
    except ConnectionError:
        Gaia3_name.append('')
    try:
        WDS_name.append(Simbad_name_string(Name[i], 'WDS'))
    except EOFError:
        WDS_name.append('')
    except TypeError:
        WDS_name.append('')
    except ConnectionError:
        WDS_name.append('')
    try:
        TMASS_name.append(Simbad_name_string(Name[i], '2MASS J'))
    except EOFError:
        TMASS_name.append('')
    except TypeError:
        TMASS_name.append('')
    except ConnectionError:
        TMASS_name.append('')
    try:
        Karmn_name.append(Simbad_name_string(Name[i], 'Karmn'))
    except EOFError:
        Karmn_name.append('')
    except TypeError:
        Karmn_name.append('')
    except ConnectionError:
        Karmn_name.append('')
    try:
        TMASS_id.append(Simbad_name_string(Name[i], '2MASS'))
    except EOFError:
        TMASS_id.append('')
    except TypeError:
        TMASS_id.append('')
    except ConnectionError:
        TMASS_id.append('')
    try:
        WISE_id.append(Simbad_name_string(Name[i], 'WISEA'))
    except EOFError:
        WISE_id.append('')
    except TypeError:
        WISE_id.append('')
    except ConnectionError:
        WISE_id.append('')

# =============================================================================
# WRITE OUT
# =============================================================================
# 'ID_star': df['col1'],
df_params = {
# 'Name': df['col1'], 'Karmn': Karmn_name,'GJ': GJ_name, 'G': G_name, 'HD': HD_name, 'NAME': NAME_name, 'LP': LP_name, \
# 'V': V_name, 'Wolf': Wolf_name, 'Ross_name': Ross_name,'BD': BD_name, 'LTT': LTT_name, 'RX': RX_name, 'PM': PM_name, 'PMJ': PMJ_name, \
'Gaia2': Gaia2_name, 'Gaia3': Gaia3_name, '2MASS': TMASS_name, 'WDS': WDS_name, 'WISE': WISE_id, '2MASS': TMASS_id}
df_append = pd.DataFrame(data=df_params)
output = pd.concat([df, df_append], axis=1)
output.to_csv('Output/'+output_file, sep=',', encoding='utf-8')
