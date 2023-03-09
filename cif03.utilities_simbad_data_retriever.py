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

ID_star = df['ID_star']
Name_star = df['Name_old']

# =============================================================================
# FUNCTION
# =============================================================================

def Simbad_data(object, data):
    """
    Finds and returns custom 'data' in Simbad.
    See all available fields with:
    Simbad.list_votable_fields()
    """
    customSimbad = Simbad()
    customSimbad.add_votable_fields('main_id', 'otype', 'otypes', 'sptype', 'sp_bibcode', 'dimensions', \
    'plx', 'plx_error', 'plx_bibcode', 'distance', 'pmra', 'pm_err_maja', 'pmdec', 'pm_err_mina', 'pm_bibcode', \
    'rvz_radvel', 'rvz_error', 'rvz_bibcode', 'fe_h')
    result = customSimbad.query_object(object)
    #
    if data == 'pmra':
        pmra = result['PMRA'][0]
        return(pmra)
    if data == 'pmra_err':
        pmra_err = result['PM_ERR_MAJA'][0]
        return(pmra_err)
    if data == 'pmdec':
        pmdec = result['PMDEC'][0]
        return(pmdec)
    if data == 'pmdec_err':
        pmdec_err = result['PM_ERR_MINA'][0]
        return(pmdec_err)
    if data == 'pm_bibcode':
        pm_bib = result['PM_BIBCODE'][0]
        return(pm_bib)
    if data == 'rv':
        rv = result['RVZ_RADVEL'][0]
        return(rv)
    if data == 'rv_err':
        rv_err = result['RVZ_ERROR'][0]
        return(rv_err)
    if data == 'rvz_bibcode':
        rv_bib = result['RVZ_BIBCODE'][0]
        return(rv_bib)
    if data == 'distance':
        distance = result['Distance_distance'][0]
        return(distance)
    if data == 'parallax':
        parallax = result['PLX_VALUE'][0]
        return(parallax)
    if data == 'parallax_err':
        parallax_err = result['PLX_ERROR'][0]
        return(parallax_err)
    if data == 'plx_bibcode':
        parallax_bib = result['PLX_BIBCODE'][0]
        return(parallax_bib)
    if data == 'object_type':
        object_type = result['OTYPE'][0]
        return(object_type)
    if data == 'object_type_ext':
        object_type_ext = result['OTYPES'][0]
        return(object_type_ext)
    if data == 'sp_type':
        sp_type = result['SP_TYPE'][0]
        return(sp_type)
    if data == 'sp_bibcode':
        sp_type_bib = result['SP_BIBCODE'][0]
        return(sp_type_bib)

# =============================================================================
# ACTION
# =============================================================================

# Simbad_data('CN Leo', 'pmra')

ID, Name, pmra, pmra_err, pmdec, pmdec_err, pm_bib, rv, rv_err, rv_bib, parallax, parallax_err, parallax_bib, distance, \
object_type, object_type_ext, sp_type, sp_type_bib = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

if 1 == 1:
    for i in range(len(df)):
    # for i in range(100): # FOR TESTING
        try:
            ID.append(int(ID_star[i]))
            Name.append(Name_star[i])
            pmra.append(Simbad_data(Name[i], 'pmra'))
            pmra_err.append(Simbad_data(Name[i], 'pmra_err'))
            pmdec.append(Simbad_data(Name[i], 'pmdec'))
            pmdec_err.append(Simbad_data(Name[i], 'pmdec_err'))
            pm_bib.append(Simbad_data(Name[i], 'pm_bibcode'))
            rv.append(Simbad_data(Name[i], 'rv'))
            rv_err.append(Simbad_data(Name[i], 'rv_err'))
            rv_bib.append(Simbad_data(Name[i], 'rvz_bibcode'))
            parallax.append(Simbad_data(Name[i], 'parallax'))
            parallax_err.append(Simbad_data(Name[i], 'parallax_err'))
            parallax_bib.append(Simbad_data(Name[i], 'plx_bibcode'))
            object_type.append(Simbad_data(Name[i], 'object_type'))
            object_type_ext.append(Simbad_data(Name[i], 'object_type_ext'))
            sp_type.append(Simbad_data(Name[i], 'sp_type'))
            sp_type_bib.append(Simbad_data(Name[i], 'sp_bibcode'))
            distance.append(Simbad_data(Name[i], 'distance'))
        except TypeError:
            pass

# =============================================================================
# WRITE OUT
# =============================================================================

output = 'y'

if output == 'y':
    df_params = {'ID_star': ID, 'Name': Name,
    'object_type': object_type, 'object_type_ext': object_type_ext,
    'sp_type': sp_type, 'sp_type_ref': sp_type_bib,
    'pmra': pmra, 'pmra_err': pmra_err, 'pmdec': pmdec, 'pmdec_err': pmdec_err, 'pm_ref': pm_bib,
    'parallax': parallax, 'parallax_err': parallax_err, 'parallax_ref': parallax_bib, 'distance': distance,
    'rv': rv, 'rv_err': rv_err, 'rv_ref': rv_bib
    }
    df_append = pd.DataFrame(data=df_params)
    # output = pd.concat([df, df_append], axis=1)
    # output.to_csv('Output/'+output_file, sep=',', encoding='utf-8')
    df_append.to_csv('Output/'+output_file, sep=',', encoding='utf-8')
else:
    pass
