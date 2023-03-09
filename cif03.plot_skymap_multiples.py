# %%

# PLOT: SKY MAP (EQUATORIAL/GALACTIC)
# Cifuentes et al. 2020

from mpl_toolkits.axes_grid1 import make_axes_locatable
from astropy.coordinates import SkyCoord
from astropy.io import ascii
import astropy.units as u
import astropy.coordinates as coord
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.cm as cm
import pandas as pd
from matplotlib import rc
from pathlib import Path

fpath = Path(matplotlib.get_data_path(), "/Users/ccifuentesr/Library/Fonts/MinionPro-MediumCapt.otf")
plt.rcParams["font.family"] = "Georgia"
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.linewidth'] = 1.5

# =============================================================================
# DATA
# =============================================================================

input_file = 'cif03.v01'
df = pd.read_csv('Data/'+input_file+'.csv', sep=",", header=0)

filter_multiple = (df['Type'] == 'Multiple')
filter_multiple_cand = (df['Type'] == 'Multiple*')
filter_single = (df['Type'] == 'Single')
filter_single_cand = (df['Type'] == 'Single*')

mult_ra = df[filter_multiple]['ra']
mult_dec = df[filter_multiple]['dec']
mult_cand_ra = df[filter_multiple_cand]['ra']
mult_cand_dec = df[filter_multiple_cand]['dec']
sing_ra = df[filter_single]['ra']
sing_dec = df[filter_single]['dec']
sing_cand_ra = df[filter_single_cand]['ra']
sing_cand_dec = df[filter_single_cand]['dec']
#
mult_equ = SkyCoord(mult_ra[:], mult_dec[:], frame='icrs', unit=(u.degree, u.degree))
mult_gal = mult_equ.galactic
mult_equ_cand = SkyCoord(mult_cand_ra[:], mult_cand_dec[:], frame='icrs', unit=(u.degree, u.degree))
mult_gal_cand = mult_equ_cand.galactic
sing_equ = SkyCoord(sing_ra[:], sing_dec[:], frame='icrs', unit=(u.degree, u.degree))
sing_gal = sing_equ.galactic
sing_equ_cand = SkyCoord(sing_cand_ra[:], sing_cand_dec[:], frame='icrs', unit=(u.degree, u.degree))
sing_gal_cand = sing_equ_cand.galactic
#
mult_equ_ra = mult_equ.ra.wrap_at(180*u.deg).radian
mult_equ_dec = mult_equ.dec.wrap_at(180*u.deg).radian
mult_equ_cand_ra = mult_equ_cand.ra.wrap_at(180*u.deg).radian
mult_equ_cand_dec = mult_equ_cand.dec.wrap_at(180*u.deg).radian
sing_equ_ra = sing_equ.ra.wrap_at(180*u.deg).radian
sing_equ_dec = sing_equ.dec.wrap_at(180*u.deg).radian
sing_equ_cand_ra = sing_equ_cand.ra.wrap_at(180*u.deg).radian
sing_equ_cand_dec = sing_equ_cand.dec.wrap_at(180*u.deg).radian

# =============================================================================
# PLOT
# =============================================================================

figsize = (12, 10)
pointsize = 30
tickssize = 22
labelsize = 22
legendsize = 18
cblabsize = 18
empty = '$\u25EF$'

fig = plt.figure(figsize=figsize)
ax = fig.add_subplot(111, projection="mollweide")
plt.grid(True)

filename = 'plot_equatorial_mult.pdf'
xlabel = r'$RA$ 'f'[deg]'
ylabel = r'$DE$ 'f'[deg]'

ax.scatter(sing_equ_ra, sing_equ_dec, s=pointsize, marker=empty, c='lightsteelblue')
ax.scatter(sing_equ_cand_ra, sing_equ_cand_dec , s=pointsize, marker=empty, c='r')
ax.scatter(mult_equ_ra, mult_equ_dec, s=pointsize, c='b')
ax.scatter(mult_equ_cand_ra, mult_equ_cand_dec, s=pointsize, c='r')


ax.set_xlabel(xlabel, size=labelsize)
ax.set_ylabel(ylabel, size=labelsize)
ax.tick_params(axis='x', labelsize=tickssize*0)
ax.tick_params(axis='y', labelsize=tickssize)

# =============================================================================
# SAVE
# =============================================================================

plt.savefig('Output/'+filename, bbox_inches='tight')
plt.show()
