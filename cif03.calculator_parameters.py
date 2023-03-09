import numpy as np
import pandas as pd
import uncertainties
import astropy
import math
from uncertainties.umath import *
import matplotlib.pyplot as plt
import astroquery
from astroquery.gaia import Gaia
from astroquery.vizier import Vizier
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
import astropy.units as u
from PyAstronomy import pyasl
import re
import csv

# =============================================================================
# CONSTANTS
# =============================================================================

Msol = 1.98847*1E30  # kg (exact)
au_m = 149597870700 # m (exact)
G = uncertainties.ufloat(6.67430*1e-11, 0.00015*1e-11) # m3 kg−1 s−2
GM = 1.3271244*1e20 # m3 s−2 (exact)

# =============================================================================
# DATA
# =============================================================================

input_file = 'cif03.v02'
output_file = input_file + '_out.csv'
df = pd.read_csv('Data/'+input_file+'.csv', sep=",", header=0)

Karmn = df['Karmn']
ID_system = df['ID_system']
ID_star = df['ID_star']
Name = df['Name']
Component = df['Component']
ra  = df['ra']
dec = df['dec']
pmra = df['pmra']
pmdec = df['pmdec']

# with open('Data/'+input_file+'.csv', 'r') as mycsv:
#     reader = csv.DictReader(mycsv)
#     ID_Gaia = []
#     for row in reader:
#         if row['GaiaDR3_id'] != 'n/a':
#             ID_Gaia.append(int(row['GaiaDR3_id']))
#         else:
#             ID_Gaia.append(0000000000)

# =============================================================================
# PARAMETERS
# =============================================================================

def param_rho(ra_1, dec_1, ra_2, dec_2):
    """Derives angular separation (rho) given the ra and dec coordinates

    Args:
        ra_1 (float): ra for star 1 in degrees
        ra_2 (float): ra for star 2 in degrees
        dec_1 (float): dec for star 1 in degrees
        dec_2 (float): dec for star 2 in degrees

    Returns:
        theta (float): rho in arcsec
    """
    c0 = SkyCoord(ra_1*u.deg, dec_1*u.deg, frame='icrs')
    c1 = SkyCoord(ra_2*u.deg, dec_2*u.deg, frame='icrs')
    sep = c0.separation(c1)
    return '{:.6f}'.format(sep.arcsecond)

def param_theta(ra_1, dec_1, ra_2, dec_2):
    """Derives positional angle (PA) given the ra and dec coordinates

    Args:
        ra_1 (float): ra for star 1 in degrees
        ra_2 (float): ra for star 2 in degrees
        dec_1 (float): dec for star 1 in degrees
        dec_2 (float): dec for star 2 in degrees

    Returns:
        theta (float): PA in degrees
    """
    theta_12= pyasl.positionAngle(ra_1, dec_1, ra_2, dec_2, positive=True)
    # theta_12 = (astropy.coordinates.position_angle(math.radians(ra_1), math.radians(dec_1), math.radians(ra_2), math.radians(dec_2))).degree
    return(theta_12)

def param_muratio(pmra_1, pmdec_1, pmra_2, pmdec_2):
    """Derives mu ratio given the proper motion in ra and dec

    Args:
        pmra_1 (float): proper motion in ra for star 1 in kms-1
        pmra_2 (float): proper motion in ra for star 2 in kms-1
        pmdec_1 (float): proper motion in dec for star 1 in kms-1
        pmdec_2 (float): proper motion in dec for star 2 in kms-1

    Returns:
        muratio (float)
    """
    muratio = sqrt(
        ((pmra_1-pmra_2)**2 + (pmdec_1-pmdec_2)**2)/(pmra_1**2 + pmdec_1**2))
    return '{:.6f}'.format(muratio)

def param_deltaPA(pmra_1, pmdec_1, pmra_2, pmdec_2):
    """Derives delta PA given the proper motion in ra and dec

    Args:
        pmra_1 (float): proper motion in ra for star 1 in kms-1
        pmra_2 (float): proper motion in ra for star 2 in kms-1
        pmdec_1 (float): proper motion in dev for star 1 in kms-1
        pmdec_2 (float): proper motion in dec for star 2 in kms-1

    Returns:
        delta PA (float)
    """
    deltaPA = degrees(
        np.abs(atan(pmdec_1/pmra_1) - atan(pmdec_2/pmra_2)))
    return '{:.6f}'.format(deltaPA)

def param_deltad(parallax_1, parallax_2):
    """Derives delta d given the parallaxes

    Args:
        parallax_1 (float): parallax for star 1 in mas
        parallax_2 (float): parallax for star 2 in mas

    Returns:
        delta d (float)
    """
    d_1 = 1000/parallax_1
    d_2 = 1000/parallax_2
    deltad = np.abs((d_1 - d_2)/d_1)
    return '{:.6f}'.format(deltad)

def param_sep(pi_mas):
    """ Calculates the search radius for a given object based on its parallactic distance.
    It is assumed a conservative maximum separation of 1E5 au.
    Args:
        pi_mas (float): Parallax in milliarcseconds.

    Returns:
        RHO (float): angular separation in arcsec.
    """
    rho = 1E5 / (1000/pi_mas)
    return rho

def Ug(s_au, Mass_A, Mass_B): 
    """  Calculates the binding energy in joules (See Sec. 3.2 in Caballero et al. 2009).
    The '*' in Ug* denotes the approximation r ~ s for small angles.

    Args:
        M1 (float): Mass of the primary in solar units.
        M2 (float): Mass of the secondary in solar units.
        rho (float): angular separation in arcsec.
        d_pc (float): distance in parsec.

    Returns:
        float: Binding energy in joules.

    Nominal solar values from the IAU B2 (AU) and B3 (GM) resolutions.
    Gravitational constant value from 2018 CODATA recommended values.
    """
    # d_pc = 1000/parallax
    # s_au = rho_arcsec * d_pc # au
    s_m = s_au * au_m # m
    Ug = G * (Mass_A*Mass_B * Msol**2)/s_m  # kg2 m2 s-2 = kg J (1 J = kg m2 s-2)
    return Ug.n, Ug.s

def Porb(s_au, Mass_A, Mass_B):
    """Calculates the orbital period in days.

    Args:
        rho (float): angular separation in arcsec.
        parallax (float): parallax in milliarcseconds.
        Mass_A (float): Mass of the primary in solar units.
        M2_Msol (float): Mass of the secondary in solar units.

    Returns:
        float: orbital period in years or days.

    Nominal solar values from the IAU B2 (AU) and B3 (GM) resolutions.
    Gravitational constant value from 2018 CODATA recommended values.
    """
    # d_pc = 1000/parallax
    # s_au = rho_arcsec * d_pc # au
    s_m = s_au * au_m # m
    mu = GM * (Mass_A + Mass_B) # m3 s-2
    Porb_s = 2*np.pi * sqrt(s_m**3/mu) # s
    Porb_d = Porb_s/86400 # d
    Porb_a = Porb_d/365.25 # a
    return(np.round(Porb_a.n,4), np.round(Porb_a.s,4))

def Mabs(mag, parallax):
    Mabs = mag - 5*log10(1000/parallax) + 5
    return Mabs

# =============================================================================
# QUERIES
# =============================================================================

def query_vizier(object, catalog, columns, radius="1s"):
    """
    Performs a query in Vizier given a valid name
    and a radius expressed as seconds.
    Choose 'full' and/or 'info' to see the entire
    table and/or the description of the rows.
    Selects first row for closest match.

    Valid catalogs: 2MASS, AllWISE
    """
    if catalog == '2MASS':
        catalog_id = 'II/246/out'
    if catalog == 'AllWISE':
        catalog_id = 'II/328/allwise'
    #
    v = Vizier(columns, catalog=catalog_id)
    try:
        result = v.query_object(object)
    except:
        pass
    return result
    #

def query_gaia(source_id):
    """Queries in Gaia Archive using ADQL syntax

    Args:
        source_id (int): unique Gaia EDR3 identificador

    Returns:
        r (astropy.table)
    """
    try:
        job = Gaia.launch_job("SELECT *"
        "FROM gaiadr3.gaia_source "
        "WHERE source_id = {id}".format(id=source_id))
    except:
        pass
    r = job.get_results()
    return r

def photometry_errors(FG, e_FG, FBP, e_FBP, FRP, e_FRP):
    """ Derives the uncertainty in apparent magnitude from the flux and its error.
    Formulae reproduced from VizieR (CDS).

    Args:
        FBP (float): Mean flux in the integrated BP band (phot_bp_mean_flux).
        FG (float): Mean flux in the integrated G band (phot_g_mean_flux).
        FRP (float): Mean flux in the integrated RP band (phot_rp_mean_flux).
        e_FBP (float): Error on the integrated BP mean flux (phot_bp_mean_flux_error).
        e_FG (float): Error on the integrated G mean flux (phot_g_mean_flux_error).
        e_FRP (float): Error on the integrated RP mean flux (phot_rp_mean_flux_error).

    Returns:
        e_BPmag (float): Error on the apparent BP magnitude.
        e_Gmag (float): Error on the apparent G magnitude.
        e_RPmag (float): Error on the apparent RP magnitude.
    """
    sigmaG_0 = 0.0027553202
    sigmaBP_0 = 0.0027901700
    sigmaRP_0 = 0.0037793818
    #
    e_BPmag = np.round(np.sqrt((-2.5/np.log(10)*e_FBP/FBP)**2 + sigmaBP_0**2), 4)
    e_Gmag = np.round(np.sqrt((-2.5/np.log(10)*e_FG/FG)**2 + sigmaG_0**2), 4)
    e_RPmag = np.round(np.sqrt((-2.5/np.log(10)*e_FRP/FRP)**2 + sigmaRP_0**2), 4)
    return(e_Gmag, e_BPmag, e_RPmag)

# =============================================================================
# PARAMETERS
# =============================================================================

# compute = 'none'
# compute = 'params'
# compute = 'catalogs'
# compute = 'gaia'
# compute = 'photometry_errors'
# compute = 'binding'
compute = 'orbital'
# compute = 'masses'
# compute = 'Mabs'

#
if compute == 'params':
    rho01 = [None, float(param_rho(ra[0], dec[0], ra[1], dec[1])), None, float(param_rho(ra[2], dec[2], ra[3], dec[3])), None, None]
    theta01 = [None, float(pyasl.positionAngle(ra[0], dec[0], ra[1], dec[1])), None, float(pyasl.positionAngle(ra[2], dec[2], ra[3], dec[3])), None, None]
    muratio01 = [None, float(param_muratio(pmra[0], pmdec[0], pmra[1], pmdec[1])), None, float(param_muratio(pmra[2], pmdec[2], pmra[3], pmdec[3])), None, None]
    deltaPA01 = [None, float(param_deltaPA(pmra[0], pmdec[0], pmra[1], pmdec[1])), None, float(param_deltaPA(pmra[2], pmdec[2], pmra[3], pmdec[3])), None, None]
    deltad01 = [None, float(param_deltad(parallax[1], parallax[0])), None, float(param_deltad(parallax[3], parallax[2])), None, None]
    rho_arcsec, theta_deg, muratio, deltaPA, deltad = [], [], [], [], []
    for i in range(6, len(df)):
        if (ID_system[i] == ID_system[i-4]):
            rho_arcsec.append(float(param_rho(ra[i], dec[i], ra[i-4], dec[i-4])))
            theta_deg.append(float(param_theta(ra[i-4], dec[i-4], ra[i], dec[i])))
            muratio.append(float(param_muratio(pmra[i], pmdec[i], pmra[i-4], pmdec[i-4])))
            deltaPA.append(float(param_deltaPA(pmra[i], pmdec[i], pmra[i-4], pmdec[i-4])))
            deltad.append(float(param_deltad(parallax[i], parallax[i-4])))
        elif (ID_system[i] == ID_system[i-3]):
            rho_arcsec.append(float(param_rho(ra[i], dec[i], ra[i-3], dec[i-3])))
            theta_deg.append(float(param_theta(ra[i-3], dec[i-3], ra[i], dec[i])))
            muratio.append(float(param_muratio(pmra[i], pmdec[i], pmra[i-3], pmdec[i-3])))
            deltaPA.append(float(param_deltaPA(pmra[i], pmdec[i], pmra[i-3], pmdec[i-3])))
            deltad.append(float(param_deltad(parallax[i], parallax[i-3])))
        elif (ID_system[i] == ID_system[i-2]):
            rho_arcsec.append(float(param_rho(ra[i], dec[i], ra[i-2], dec[i-2])))
            theta_deg.append(float(param_theta(ra[i-2], dec[i-2], ra[i], dec[i])))
            muratio.append(float(param_muratio(pmra[i], pmdec[i], pmra[i-2], pmdec[i-2])))
            deltaPA.append(float(param_deltaPA(pmra[i], pmdec[i], pmra[i-2], pmdec[i-2])))
            deltad.append(float(param_deltad(parallax[i], parallax[i-2])))
        elif (ID_system[i] == ID_system[i-1]):
            rho_arcsec.append(float(param_rho(ra[i], dec[i], ra[i-1], dec[i-1])))
            theta_deg.append(float(param_theta(ra[i-1], dec[i-1], ra[i], dec[i])))
            muratio.append(float(param_muratio(pmra[i], pmdec[i], pmra[i-1], pmdec[i-1])))
            deltaPA.append(float(param_deltaPA(pmra[i], pmdec[i], pmra[i-1], pmdec[i-1])))
            deltad.append(float(param_deltad(parallax[i], parallax[i-1])))
        else:
            rho_arcsec.append(None)
            theta_deg.append(None)
            muratio.append(None)
            deltaPA.append(None)
            deltad.append(None)

    rho_arcsec = rho01+rho_arcsec
    theta_deg = theta01+theta_deg
    muratio = muratio01+muratio
    deltaPA = deltaPA01+deltaPA
    deltad = deltad01+deltad
    #
    df_results = {'ID_star': df['ID_star'], 'rho_arcsec': rho_arcsec,\
    'theta_deg': theta_deg, 'muratio': muratio, 'deltaPA': deltaPA, 'deltad': deltad}
elif compute == 'catalogs':
    get_TMASS = ['RAJ2000', 'DEJ2000', 'Jmag', 'e_Jmag', 'Hmag', 'e_Hmag', 'Kmag', 'e_Kmag', 'Qflg', '+_r']
    get_AllWISE = ['W1mag', 'e_W1mag', 'W2mag', 'e_W2mag', 'W3mag', 'e_W3mag', 'W4mag', 'e_W4mag', 'qph', 'AllWISE', '2M', '+_r']
    params_TMASS = [[] for _ in get_TMASS]
    params_AllWISE = [[] for _ in get_AllWISE]
    #
    for j in range(len(get_TMASS)):
        for i in range(len(df)):
            try:
                print(df['2MASS_id'][i], query_vizier('J'+str(df['2MASS_id'][i]), '2MASS', get_TMASS)[0][get_TMASS[j]][0])
                params_TMASS[j].append(query_vizier('J'+str(df['2MASS_id'][i]), '2MASS', get_TMASS)[0][get_TMASS[j]][0])
            except:
                print(df['2MASS_id'][i], 'Not found')
                params_TMASS[j].append(None)
    df_results = {'ID_star': df['ID_star'], 'RAJ2000': params_TMASS[0], 'DEJ2000': params_TMASS[1],\
    'Jmag': params_TMASS[2], 'eJmag': params_TMASS[3], 'Hmag': params_TMASS[4], 'eHmag': params_TMASS[5],\
    'Kmag': params_TMASS[6], 'eKmag': params_TMASS[7], 'Qflg': params_TMASS[8]}

    # for j in range(len(get_AllWISE)):
    #     for i in range(len(df)):
    #         try:
    #             print(df['allWISE_id'][i], query_vizier(str(df['allWISE_id'][i]), 'AllWISE', get_AllWISE)[0][get_AllWISE[j]][0])
    #             params_AllWISE[j].append(query_vizier(str(df['allWISE_id'][i]), 'AllWISE', get_AllWISE)[0][get_AllWISE[j]][0])
    #         except:
    #             print(df['allWISE_id'][i], 'Not found')
    #             params_AllWISE[j].append(None)
    # df_results = {'ID_star': df['ID_star'], 'W1mag': params_AllWISE[0], 'e_W1mag': params_AllWISE[1],\
    # 'W2mag': params_AllWISE[2], 'e_W2mag': params_AllWISE[3], 'W3mag': params_AllWISE[4], 'e_W3mag': params_AllWISE[5],\
    # 'W4mag': params_AllWISE[6], 'e_W4mag': params_AllWISE[7], 'qph': params_AllWISE[8], 'AllWISE': params_AllWISE[9]}
elif compute == 'gaia':
    astroquery.simbad.conf.server
    Gaia.login(user='ccifuent', password='***')
    #
    get_Gaia = ['ra', 'ra_error', 'dec', 'dec_error', 'l', 'b',\
    'parallax', 'parallax_error', 'pmra', 'pmra_error', 'pmdec', 'pmdec_error', \
    'astrometric_excess_noise', 'astrometric_excess_noise_sig', 'astrometric_n_obs_al', 'astrometric_n_good_obs_al',\
    'ipd_gof_harmonic_amplitude', 'duplicated_source', 'non_single_star', \
    'phot_g_mean_flux', 'phot_g_mean_flux_error', 'phot_g_mean_mag', 'phot_bp_mean_flux', 'phot_bp_mean_flux_error',\
    'phot_bp_mean_mag', 'phot_rp_mean_flux', 'phot_rp_mean_flux_error', 'phot_rp_mean_mag', 'phot_bp_rp_excess_factor',\
    'phot_bp_n_blended_transits', 'phot_rp_n_blended_transits', 'phot_variable_flag',\
    'radial_velocity', 'radial_velocity_error', 'rv_chisq_pvalue', 'rv_amplitude_robust', 'rv_nb_transits', 'rv_renormalised_gof', 'ruwe']
    #
    params_Gaia = [[] for _ in get_Gaia]
    for i in range(1):
        print('Star', i, 'in progress...')
        for j in range(len(get_Gaia)):
            try:
                query = query_gaia(ID_Gaia[i])
                params_Gaia[j].append(query[get_Gaia[j]][0])
            except:
                params_Gaia[j].append(None)
    #
    phot_errors = 'no'
    if phot_errors == 'yes':
        eG, eBP, eRP = [], [], []
        for i in range(len(df)):
            for j in range(len(get_Gaia)):
                try:
                    phot_err = photometry_errors(params_Gaia[19][i], params_Gaia[20][i], params_Gaia[22][i], params_Gaia[23][i], params_Gaia[25][i], params_Gaia[26][i])
                    eG.append(phot_err[0])
                    eBP.append(phot_err[1])
                    eRP.append(phot_err[2])
                except:
                    eG.append(None)
                    eBP.append(None)
                    eRP.append(None)
        df_results = {'ID_star': df['ID_star'], 'phot_g_mean_mag_error': eG, 'phot_rp_mean_mag_error': eRP, 'phot_bp_mean_mag_error': eBP}
    else:
        pass
    # 'ID_star': df['ID_star'], 'GaiaDR3_id': ID_Gaia,
    df_results = {'ra': params_Gaia[0], 'ra_error': params_Gaia[1], 'dec': params_Gaia[2],\
    'dec_error': params_Gaia[3], 'l': params_Gaia[4], 'b': params_Gaia[5], 'parallax': params_Gaia[6], 'parallax_error': params_Gaia[7],\
    'pmra': params_Gaia[8], 'pmra_error': params_Gaia[9], 'pmdec': params_Gaia[10], 'pmdec_error': params_Gaia[11],\
    'astrometric_excess_noise': params_Gaia[12], 'astrometric_excess_noise_sig': params_Gaia[13], 'astrometric_n_obs_al': params_Gaia[14],\
    'astrometric_n_good_obs_al': params_Gaia[15], 'ipd_gof_harmonic_amplitude': params_Gaia[16], 'duplicated_source': params_Gaia[17],\
    'non_single_star': params_Gaia[18], 'phot_g_mean_mag': params_Gaia[21],\
    'phot_bp_mean_mag': params_Gaia[24], 'phot_rp_mean_mag': params_Gaia[27],\
    'phot_bp_rp_excess_factor': params_Gaia[28], 'phot_bp_n_blended_transits': params_Gaia[29],\
    'phot_rp_n_blended_transits': params_Gaia[30], 'phot_variable_flag': params_Gaia[31], 'radial_velocity': params_Gaia[32],\
    'radial_velocity_error': params_Gaia[33], 'rv_chisq_pvalue': params_Gaia[34], 'rv_amplitude_robust': params_Gaia[35],\
    'rv_nb_transits': params_Gaia[36], 'rv_renormalised_gof': params_Gaia[37], 'ruwe': params_Gaia[38]}
elif compute == 'photometry_errors':
    phot_g_mean_flux = df['phot_g_mean_flux']
    phot_g_mean_flux_error = df['phot_g_mean_flux_error']
    phot_bp_mean_flux = df['phot_bp_mean_flux']
    phot_bp_mean_flux_error = df['phot_bp_mean_flux_error']
    phot_rp_mean_flux = df['phot_rp_mean_flux']
    phot_rp_mean_flux_error = df['phot_rp_mean_flux_error']
    #
    eG_mag, eBP_mag, eRP_mag = [], [], []
    for i in range(len(df)):
        errors = photometry_errors(phot_g_mean_flux[i], phot_g_mean_flux_error[i], phot_bp_mean_flux[i], \
        phot_bp_mean_flux_error[i], phot_rp_mean_flux[i], phot_rp_mean_flux_error[i])
        eG_mag.append(errors[0])
        eBP_mag.append(errors[1])
        eRP_mag.append(errors[2])
    df_results = {'karmn': df['karmn'], 'phot_g_mean_mag': eG_mag, 'phot_bp_mean_mag_error': eBP_mag, 'phot_rp_mean_mag_error': eRP_mag}
elif compute == 'binding':
    Mass_A = [uncertainties.ufloat(df['Mass_A'][i], df['eMass_A'][i]) for i in range(len(df))]
    Mass_B = [uncertainties.ufloat(df['Mass_B'][i], df['eMass_B'][i]) for i in range(len(df))]
    parallax = [uncertainties.ufloat(df['parallax'][i], df['parallax_error'][i]) for i in range(len(df))]
    rho_arcsec = df['rho01']
    a_au = df['s01']
    #
    Ug_J, eUg_J = [], []
    for i in range(len(df)):
        try:
            Ug_J.append(Ug(a_au[i], Mass_A[i], Mass_B[i])[0]) #rho_arcsec[i], parallax[i], 
            eUg_J.append(Ug(a_au[i], Mass_A[i], Mass_B[i])[1]) #rho_arcsec[i], parallax[i], 
        except:
            Ug_J.append(np.nan)
            eUg_J.append(np.nan)
    #
    df_results = {'ID_star': df['ID_star'], 'Ug_J': Ug_J, 'eUg_J': eUg_J}
elif compute == 'orbital':
    Mass_A = [uncertainties.ufloat(df['Mass_A'][i], df['eMass_A'][i]) for i in range(len(df))]
    Mass_B = [uncertainties.ufloat(df['Mass_B'][i], df['eMass_B'][i]) for i in range(len(df))]
    parallax = [uncertainties.ufloat(df['parallax'][i], df['parallax_error'][i]) for i in range(len(df))]
    rho_arcsec = df['rho01']
    a_au = df['s01']
    #
    Porb_d, ePorb_d = [], []
    for i in range(len(df)):
        try:
            Porb_d.append(Porb(a_au[i], Mass_A[i], Mass_B[i])[0]) # rho_arcsec[i], parallax[i]
            ePorb_d.append(Porb(a_au[i], Mass_A[i], Mass_B[i])[1]) # rho_arcsec[i], parallax[i]
        except:
            Porb_d.append(np.nan)
            ePorb_d.append(np.nan)
    #
    df_results = {'ID_star': df['ID_star'], 'Porb_d': Porb_d, 'ePorb_d': ePorb_d}
elif compute == 'masses':
    Mass_A = [uncertainties.ufloat(df['Mass_A'][i], df['eMass_A'][i]) for i in range(len(df))]
    #
    Mratio01 = [None, Mass_A[1].n/Mass_A[0].n, None, Mass_A[3].n/Mass_A[2].n, None, None]
    Mtotal01 = [None, Mass_A[1].n + Mass_A[0].n, None, Mass_A[3].n + Mass_A[2].n, None, None]
    Mtotal01_error = [None, np.sqrt(Mass_A[1].s**2 + Mass_A[0].s**2), None, np.sqrt(Mass_A[3].s**2 + Mass_A[2].s**2), None, None]
    Mratio, Mt_Msol, eMt_Msol = [], [], []
    for i in range(6, len(df)):
        if (ID_system[i] == ID_system[i-4]):
            Mratio.append(Mass_A[i].n/Mass_A[i-4].n)
            Mt_Msol.append(Mass_A[i].n + Mass_A[i-4].n)
            eMt_Msol.append(np.sqrt(Mass_A[i].s**2 + Mass_A[i-4].s**2))
        elif (ID_system[i] == ID_system[i-3]):
            Mratio.append(Mass_A[i].n/Mass_A[i-3].n)
            Mt_Msol.append(Mass_A[i].n + Mass_A[i-3].n)
            eMt_Msol.append(np.sqrt(Mass_A[i].s**2 + Mass_A[i-3].s**2))
        elif (ID_system[i] == ID_system[i-2]):
            Mratio.append(Mass_A[i].n/Mass_A[i-2].n)
            Mt_Msol.append(Mass_A[i].n + Mass_A[i-2].n)
            eMt_Msol.append(np.sqrt(Mass_A[i].s**2 + Mass_A[i-2].s**2))
        elif (ID_system[i] == ID_system[i-1]):
            Mratio.append(Mass_A[i].n/Mass_A[i-1].n)
            Mt_Msol.append(Mass_A[i].n + Mass_A[i-1].n)
            eMt_Msol.append(np.sqrt(Mass_A[i].s**2 + Mass_A[i-1].s**2))
        else:
            Mratio.append(None)
            Mt_Msol.append(None)
            eMt_Msol.append(None)

    Mratio = Mratio01+Mratio
    Mt_Msol = Mtotal01+Mt_Msol
    eMt_Msol = Mtotal01_error+eMt_Msol
    #
    df_results = {'ID_star': df['ID_star'], 'q_all': Mratio, 'Mt_Msol': Mt_Msol, 'eMt_Msol': eMt_Msol}
elif compute == 'Mabs':
    G_mag = [uncertainties.ufloat(df['G_mag'][i], df['eG_mag'][i]) for i in range(len(df))]
    parallax = [uncertainties.ufloat(df['parallax'][i], df['parallax_error'][i]) for i in range(len(df))]
    Mabs = [Mabs(G_mag[i],parallax[i]) for i in range(len(df))]
    MG = [Mabs[i].n for i in range(len(df))]
    eMG = [Mabs[i].s for i in range(len(df))]
    #
    df_results = {'ID_star': df['ID_star'], 'MG_mag': MG, 'eMG_mag': eMG}
else:
    pass

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
