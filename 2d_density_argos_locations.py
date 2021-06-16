from argopy import DataFetcher as ArgoDataFetcher
from mpl_toolkits.basemap import Basemap

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as colors

mpl.use('Agg')

argo_loader = ArgoDataFetcher()

fig = plt.figure(figsize=(6,7)) 

m = Basemap(projection='lcc', resolution='h', lat_0=43, lon_0=145, width=2E6, height=3E6)

m.shadedrelief()
m.drawcoastlines(color='gray')
m.drawcountries(color='gray')

ds_points = argo_loader.region([140, 150, 35, 50, 0, 100, '2015-06-01', '2015-12-30']).to_xarray()
ds = ds_points.argo.point2profile()
df = ds.to_dataframe()
df = df.reset_index()
df = df[['LATITUDE','LONGITUDE']]
x,y = m(df['LONGITUDE'], df['LATITUDE'])

thiscmap = plt.cm.get_cmap('viridis')

m.hexbin(x, y, gridsize=[6,6], mincnt=1, cmap='summer', norm=colors.LogNorm(), alpha=0.4) 
cbar = plt.colorbar() 
cbar.ax.set_ylabel('# of profiles', rotation=270, fontsize = 15)

lats = [43.0618,35.6762,38.2682,44.0958]
lons = [141.3545,139.6503,140.8694,145.8336]
names = ['Sapporo','Tokyo','Sendai','Kunashiri']
x, y = m(lons, lats)
m.scatter(x, y, 20, color="black", marker="o", edgecolor="k")
for i in range(len(names)):
    plt.text(x[i], y[i], names[i])

plt.savefig("hexbin_argos_locations.png")