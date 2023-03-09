import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from astroquery.gaia import Gaia

Gaia.login(user='ccifuent', password='***')

# Data

version = '05'
input_name = 'cif03.v' + version
output_name = input_name + '_out.csv'

df = pd.read_csv('Data/'+input_name+'.csv')

ra_search = df['ra_1']
dec_search = df['dec_1']
parallax_search = df['parallax']

def rho(pi_mas):
    """ Calculates the search radius for a given object based on its parallactic distance.
    It is assumed a conservative maximum separation of 1E5 au.
    Args:
        pi_mas (float): Parallax in milliarcseconds.

    Returns:
        float: angular separation in arcsec.
    """
    rho = 1E5 / (1000/pi_mas)
    return rho

# %%

start = time.time()

Karmn = [[] for i in range(len(df))]
Name = [[] for i in range(len(df))]
source_id = [[] for i in range(len(df))]
ra = [[] for i in range(len(df))]
ra_error = [[] for i in range(len(df))]
dec = [[] for i in range(len(df))]
dec_error = [[] for i in range(len(df))]
parallax = [[] for i in range(len(df))]
parallax_error = [[] for i in range(len(df))]
pmra = [[] for i in range(len(df))]
pmra_error = [[] for i in range(len(df))]
pmdec = [[] for i in range(len(df))]
pmdec_error = [[] for i in range(len(df))]
pm = [[] for i in range(len(df))]
dr2_radial_velocity = [[] for i in range(len(df))]
dr2_radial_velocity_error = [[] for i in range(len(df))]
ruwe = [[] for i in range(len(df))]
phot_bp_mean_mag = [[] for i in range(len(df))]
phot_g_mean_mag = [[] for i in range(len(df))]
phot_rp_mean_mag = [[] for i in range(len(df))]
dist = [[] for i in range(len(df))]
#
mu_ratio = [[] for i in range(len(df))]
delta_PA = [[] for i in range(len(df))]
delta_d = [[] for i in range(len(df))]
phot_bp_mean_mag_error = [[] for i in range(len(df))]
phot_g_mean_mag_error = [[] for i in range(len(df))]
phot_rp_mean_mag_error = [[] for i in range(len(df))]
dictionary = [[] for i in range(len(df))]

#
for i in range(0,10): #len(df)
    query = (
        """SELECT * , distance(POINT('ICRS', {ra}, {dec}), POINT('ICRS', gaia.ra, gaia.dec))
        AS dist FROM gaiaedr3.gaia_source AS gaia WHERE 1=CONTAINS(POINT('ICRS', {ra}, {dec}),
        CIRCLE('ICRS', gaia.ra, gaia.dec, {r})) AND abs(1-(gaia.parallax/{parallax})) < 0.10)""".format(ra=ra_search[i], dec=dec_search[i], r=rho(parallax_search[i])/3600, parallax = parallax_search[i])
        )
    job = Gaia.launch_job_async(query=query)
    results = job.get_results()
    for j in range(len(results['source_id'])):
        print('Computing system', i, j)
    # Append parameters for each query
        Karmn[i].append(df['Karmn'][i])
        Name[i].append(df['Name'][i])
        source_id[i].append(results[j]['source_id'])
        ra[i].append(results[j]['ra'])
        ra_error[i].append(results[j]['ra_error'])
        dec[i].append(results[j]['dec'])
        dec_error[i].append(results[j]['dec_error'])
        parallax[i].append(results[j]['parallax'])
        parallax_error[i].append(results[j]['parallax_error'])
        pmra[i].append(results[j]['pmra'])
        pmra_error[i].append(results[j]['pmra_error'])
        pmdec[i].append(results[j]['pmdec'])
        pmdec_error[i].append(results[j]['pmdec_error'])
        pm[i].append(results[j]['pm'])
        dr2_radial_velocity[i].append(results[j]['dr2_radial_velocity'])
        dr2_radial_velocity_error[i].append(results[j]['dr2_radial_velocity_error'])
        ruwe[i].append(results[j]['ruwe'])
        phot_bp_mean_mag[i].append(results[j]['phot_bp_mean_mag'])
        phot_g_mean_mag[i].append(results[j]['phot_g_mean_mag'])
        phot_rp_mean_mag[i].append(results[j]['phot_rp_mean_mag'])
        dist[i].append(results[j]['dist'])
        mu_ratio[i].append(muratio(results['pmra'][0], results['pmra'][j], results['pmdec'][0], results['pmdec'][j]))
        delta_PA[i].append(deltaPA(results['pmra'][0], results['pmra'][j], results['pmdec'][0], results['pmdec'][j]))
        delta_d[i].append(deltad(results['parallax'][0], results['parallax'][j]))
        photometry_err = phot_errors(results['phot_bp_mean_flux'][j], results['phot_bp_mean_flux_error'][j], results['phot_g_mean_flux'][j],
            results['phot_g_mean_flux_error'][j], results['phot_rp_mean_flux'][j], results['phot_rp_mean_flux_error'][j])
        phot_bp_mean_mag_error[i].append(photometry_err[0])
        phot_g_mean_mag_error[i].append(photometry_err[1])
        phot_rp_mean_mag_error[i].append(photometry_err[2])
    #
        dictionary[i].append({'Karmn': Karmn[i][j], 'Name': Name[i][j], 'source_id': source_id[i][j], 'ruwe': ruwe[i][j], 'dist':  dist[i][j]})
        dictionary[i].append({k:[v] for k,v in dictionary[i][0].items()})
        # df_out = pd.DataFrame(dictionary[i])
        # output = pd.concat([df, MR], axis=1)
        # df_out.to_csv(output_name, sep=',', encoding='utf-8')
    print(f"\nGaia EDR3 query for Karmn {df['Karmn'][i]} in a radius of {np.round(rho(pi_mas[i]), 2)} arcsec:\n\n {results}")

end = time.time()
print(f"\nRuntime: {np.round(end - start,2)} seconds.")

#

dictionary = [[] for i in range(len(df))]

for i in range(0, 2):
    for j in range(len(results['source_id'])):
        dictionary[i].append({'Karmn': Karmn[i][j], 'Name': Name[i][j], 'source_id': source_id[i][j], 'ruwe': ruwe[i][j], 'dist':  dist[i][j]})
        dictionary[i].append({k:[v] for k,v in dictionary[i][0].items()})
        df_out = pd.DataFrame(dictionary[i])
        # output = pd.concat([df, MR], axis=1)
        df_out.to_csv(output_name, sep=',', encoding='utf-8')

# %%

source_id_ = [[] for i in range(0,3)]

for i in range(0,3): #len(source_id)
    for j in range(len(source_id[i])):
        source_id_[i].append(Karmn[i][j])
        source_id_[i].extend(
            [Name[i][j],
            source_id[i][j],
            parallax[i][j],
            parallax_error[i][j],
            pmra[i][j],
            pmra_error[i][j],
            pmdec[i][j],
            pmdec_error[i][j],
            pm[i][j],
            dr2_radial_velocity[i][j],
            dr2_radial_velocity_error[i][j],
            ruwe[i][j],
            phot_bp_mean_mag[i][j],
            phot_g_mean_mag[i][j],
            phot_rp_mean_mag[i][j],
            dist[i][j],
            mu_ratio[i][j],
            delta_PA[i][j],
            delta_d[i][j],
            phot_bp_mean_mag_error[i][j],
            phot_g_mean_mag_error[i][j],
            phot_rp_mean_mag_error[i][j]]
            )

# %%

for index, row in df.iterrows():
    print(row['Karmn'], row['parallax_edr3_1'])

# %%
# Plotting

parallax_ratio = []

for i in range(len(source_id)):
    parallax_ratio.append(np.abs(parallax[i]/pi_mas))

#

df = results.to_pandas()
df.insert(10, "parallax_ratio", parallax_ratio) # adds as a new column
# df.drop('parallax_ratio', inplace=True, axis=1) # removes column

candidates = df[(df['parallax_ratio'] > 0.8) & (df['parallax_ratio'] < 1.2)]

x = G_mag
y = parallax_ratio

# Sizes

figsize = (12, 10)
pointsize = 30
tickssize = 22
labelsize = 22
legendsize = 18
cblabsize = 18

# Canvas & Colours

fig = plt.figure(figsize=figsize)
ax = fig.add_subplot(111)
plt.grid(False)

cmap = plt.get_cmap('magma_r')

# Plots

ax.scatter(x, y, s=pointsize, c='none',edgecolors='k') #, c=z, cmap=cmap)

# Filling

x_shadow = np.linspace(0.5*min(x), 10*max(x), 100)
plt.fill_between(x_shadow, 0.8, 1.2, color='Blue', alpha=0.1, zorder=0)

ax.axhline(1.0, color='black', lw=2, alpha=0.15)

# Labels

xlabel = r'$G$ [mag]'
# xlabel = r'$\mu$ [mas a${-1}$]'
ylabel = r'$\pi/\pi_A$'

# Axes

ax.set_xlabel(xlabel, size=labelsize)
ax.set_ylabel(ylabel, size=labelsize)
ax.tick_params(axis='x', labelsize=tickssize)
ax.tick_params(axis='y', labelsize=tickssize)

ax.tick_params(axis='x', labelsize=tickssize, direction='in',
               top=True, labeltop=False, which='both')
ax.tick_params(axis='y', labelsize=tickssize, direction='in',
               right=True, labelright=False, which='both')
ax.tick_params('both', length=10, width=1, which='major')
ax.tick_params('both', length=5, width=1, which='minor')
ax.minorticks_on()
ax.xaxis.set_tick_params(which='minor', bottom=True, top=True)

# ax.set_xscale('log')

ax.set_xlim(0.9*min(x), 1.1*max(x))
ax.set_ylim(0.0, 1.2*max(y))

# Colorbar

# divider = make_axes_locatable(plt.gca())
# cax = divider.append_axes("right", "2%", pad="1%")
# cbar = plt.colorbar(sc, cax=cax)  # Colorbar
# cbar.set_label(cbarlabel, rotation=270, fontsize=labelsize, labelpad=30)
# sc.set_clim(vmin=-2, vmax=18)  # Keep uncommented to hide the colorbar
# cbar.set_ticks(np.arange(-2, 19, 2))
# cbar.ax.set_yticklabels(SpT_half)
# cbar.ax.tick_params(labelsize=cblabsize)
# cbar.outline.set_visible(False)

# Show & Save

filename = 'test'
# plt.savefig(filename+'.png', bbox_inches='tight')
plt.show()
