import numpy as np
import pandas as pd
import uncertainties
from uncertainties.umath import *
import matplotlib.pyplot as plt
import astroquery
from astroquery.gaia import Gaia
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
import astropy.units as u
from PyAstronomy import pyasl
import re
astroquery.simbad.conf.server

# See functions of umath in: shorturl.at/yPVW6 (robinlombaert.github.io)

# =============================================================================
# DATA
# =============================================================================

input_file = 'cif03.v09'
output_file = input_file + '_out.csv'
df = pd.read_csv('Data/'+input_file+'.csv', sep=",", header=0)
def query_gaia(source_id):
    """Queries in Gaia Archive using ADQL syntax

    Args:
        source_id (int): unique Gaia EDR3 identificador

    Returns:
        r (astropy.table)
    """
    Gaia.login(user='ccifuent', password='***')
    job = Gaia.launch_job("SELECT ra, dec, pmra, pmdec, parallax "
                          "FROM gaiaedr3.gaia_source "
                          "WHERE source_id = {id}".format(id=source_id))
    r = job.get_results()
    return r
