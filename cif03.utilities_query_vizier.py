import numpy as np
import pandas as pd
from astroquery.simbad import Simbad
from astroquery.vizier import Vizier

# file = 'cif03.v06'
# df = pd.read_csv('Data/'+file+'.csv', sep=",", header=0, nrows=2)

def query_vizier(name, catalog_id): # catalog, radius="10s", info=0
    """
    Performs a query in Vizier given a valid name
    and a radius expressed as seconds.
    Choose 'full' and/or 'info' to see the entire
    table and/or the description of the rows.
    Selects first row for closest match.

    Valid catalogs: 2MASS, AllWISE
    """
    if catalog_id == '2MASS':
        catalog_id = 'II/246/out'
        columns = ['RAJ2000', 'DEJ2000', 'Jmag', 'e_Jmag', 'Hmag', 'e_Hmag', 'Kmag', 'e_Kmag', 'Qflg']
    if catalog_id == 'AllWISE':
        catalog_id = 'II/328/allwise'
        columns = ['W1mag', 'eW1mag', 'W2mag', 'eW2mag', 'W3mag', 'eW3mag', 'W4mag', 'eW4mag']
    #
    v = Vizier(columns, catalog=catalog_id)
    try:
        result = v.query_object(name)
    except:
        pass
        # raise TypeError("Not found")
    return result[0] # USe also return result.info()

name = '2MASS J'+str(df['2MASS_id'][0])
test = query_vizier(name, 'AllWISE')
print(test)

query_vizier(input('Name: '))

results_2MASS = []

for i in range(len(id_2MASS)):
    # print('2MASS J'+str(id_2MASS[i]))
    results_2MASS.append(query_vizier('2MASS J'+str(id_2MASS[i]), '2MASS'))
    # query_vizier()

print(query_vizier('GJ 357', '2MASS'))

# query_2MASS = []
# for i in range(len(df)):
#     id_2MASS = '2MASS J'+str(df['2MASS_id'][i])
#     print(id_2MASS)
#     query_2MASS.append(query_vizier(id_2MASS, '2MASS'))
# # print(name)
# # # print(query_simbad(name))
# print(query_2MASS)
