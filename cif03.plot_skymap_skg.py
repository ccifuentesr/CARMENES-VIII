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

SKG_list01 = ['beta Pic', 'Castor', 'Columba',  'LA', 'IC2391', 'Her-Lyr', 'Pleiades']
SKG_ra01 = [df[df['SKG'].str.contains(SKG_list01[i]) == True]['ra'] for i in range(len(SKG_list01))]
SKG_dec01 = [df[df['SKG'].str.contains(SKG_list01[i]) == True]['dec'] for i in range(len(SKG_list01))]
SKG_SpTnum01 = [df[df['SKG'].str.contains(SKG_list01[i]) == True]['SpTnum'] for i in range(len(SKG_list01))]
size01 = [df[df['SKG'].str.contains(SKG_list01[i]) == True]['MG_mag'] for i in range(len(SKG_list01))]
#
SKG_list02 = ['UMa', 'Taurus', 'Hyades', 'Argus', 'Carina', 'Tuc-Hor', 'AB Dor']
SKG_ra02 = [df[df['SKG'].str.contains(SKG_list02[i]) == True]['ra'] for i in range(len(SKG_list02))]
SKG_dec02 = [df[df['SKG'].str.contains(SKG_list02[i]) == True]['dec'] for i in range(len(SKG_list02))]
SKG_SpTnum02 = [df[df['SKG'].str.contains(SKG_list02[i]) == True]['SpTnum'] for i in range(len(SKG_list02))]
size02 = [df[df['SKG'].str.contains(SKG_list02[i]) == True]['MG_mag'] for i in range(len(SKG_list02))]
#
SKG_equatorial01 = [SkyCoord(SKG_ra01[i][:], SKG_dec01[i][:], frame='icrs',
    unit=(u.degree, u.degree)) for i in range(len(SKG_list01))]
SKG_galactic01 = [SKG_equatorial01[i].galactic for i in range(len(SKG_list01))]
SKG_equatorial_ra01 = [SKG_equatorial01[i].ra.wrap_at(180*u.deg).radian for i in range(len(SKG_list01))]
SKG_equatorial_dec01 = [SKG_equatorial01[i].dec.wrap_at(180*u.deg).radian for i in range(len(SKG_list01))]
SKG_galactic_l01 = [SKG_galactic01[i].l.wrap_at(180*u.deg).radian  for i in range(len(SKG_list01))]
SKG_galactic_b01 = [SKG_galactic01[i].b.wrap_at(180*u.deg).radian  for i in range(len(SKG_list01))]
#
SKG_equatorial02 = [SkyCoord(SKG_ra02[i][:], SKG_dec02[i][:], frame='icrs',
    unit=(u.degree, u.degree)) for i in range(len(SKG_list02))]
SKG_galactic02 = [SKG_equatorial02[i].galactic for i in range(len(SKG_list02))]
SKG_equatorial_ra02 = [SKG_equatorial02[i].ra.wrap_at(180*u.deg).radian for i in range(len(SKG_list02))]
SKG_equatorial_dec02 = [SKG_equatorial02[i].dec.wrap_at(180*u.deg).radian for i in range(len(SKG_list02))]
SKG_galactic_l02 = [SKG_galactic02[i].l.wrap_at(180*u.deg).radian  for i in range(len(SKG_list02))]
SKG_galactic_b02 = [SKG_galactic02[i].b.wrap_at(180*u.deg).radian  for i in range(len(SKG_list02))]

# =============================================================================
# PLOT
# =============================================================================

figsize = (12, 10)
pointsize = 30
tickssize = 22
labelsize = 22
legendsize = 18
cblabsize = 18

# plt.style.use('dark_background')

fig = plt.figure(figsize=figsize)
ax = fig.add_subplot(111, projection="mollweide", facecolor='#2D2D2D')
plt.grid(True)

cmap01 = plt.get_cmap('tab10')
cmap02 = plt.get_cmap('tab10_r')
SKG_colors01 = [cmap01(i/len(SKG_list01)) for i in range(len(SKG_list01))]
SKG_colors02 = [cmap02(i/len(SKG_list02)) for i in range(len(SKG_list02))]

filename = 'plot_equatorial_skg.pdf'
xlabel = r'$RA$ 'f'[deg]'
ylabel = r'$DE$ 'f'[deg]'

plot = 'equatorial'

if plot == 'equatorial':
    x01 = SKG_equatorial_ra01
    y01 = SKG_equatorial_dec01
    z01 = SKG_colors01
    s01 = size01
    #
    x02 = SKG_equatorial_ra02
    y02 = SKG_equatorial_dec02
    z02 = SKG_colors02
    s02 = size02

if plot == 'galactic':
    x01 = SKG_galactic_l01
    y01 = SKG_galactic_b01
    z01 = SKG_colors01
    s01 = size01
    #
    x02 = SKG_galactic_l02
    y02 = SKG_galactic_b02
    z02 = SKG_colors02
    s02 = size02

for i in range(len(SKG_list01)):
    sc01 = ax.scatter(x01[i], y01[i], s=s01[i]*3.5, c=z01[i], label = SKG_list01[i], zorder=1)
    sc02 = ax.scatter(x02[i], y02[i], s=s02[i]*3.5, c=z02[i], label = SKG_list02[i], zorder=1)

ax.set_xlabel(xlabel, size=labelsize)
ax.set_ylabel(ylabel, size=labelsize)
ax.tick_params(axis='x', labelsize=tickssize*0.8)
ax.tick_params(axis='y', labelsize=tickssize)
ax.xaxis.label.set_color('white')
ax.tick_params(axis='x', colors='white')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, +0.25),
          fancybox=True, shadow=False, ncol=5)

# divider = make_axes_locatable(plt.gca())
# cax = divider.append_axes("right", "2%", pad="1%")
# cbar = plt.colorbar(sc, cax=cax)  # Colorbar
# cbar.set_label(cbarlabel, rotation=270, fontsize=labelsize, labelpad=30)
# sc.set_clim(vmin=70, vmax=80)
# cbar.set_ticks(np.arange(-2, 19, 2))
# cbar.ax.set_yticklabels(SpT_half)
# cbar.ax.tick_params(labelsize=cblabsize)
# cbar.outline.set_visible(False)

# =============================================================================
# SAVE
# =============================================================================

plt.savefig('Output/'+filename, bbox_inches='tight')
plt.show()
