from argopy import DataFetcher as ArgoDataFetcher   # For fetching argo data
from scipy.stats import pearsonr
from mpl_toolkits.basemap import Basemap    # For map generation
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns   # For plotting

#Needed to save figures in wsl environment
mpl.use('Agg')


def reg_coef(x,y,label=None,color=None,**kwargs):
    '''Plots the pearsonr coefficient for each pair
    of variables. To be used for upper diagonal of
    the correlation plot.
    '''
    ax = plt.gca()
    r,p = pearsonr(x,y)
    ax.annotate('r = {:.2f}'.format(r), xy=(0.5,0.5), xycoords='axes fraction', ha='center', fontsize=25)
    ax.set_axis_off()

mpl.rcParams["axes.labelsize"] = 20 # Enlarging the size of pearsonr coefficients appearing on the plot

argo_loader = ArgoDataFetcher()

#Fething argo data. For details, refer to the final report.
ds_points1 = argo_loader.profile(5905775, 1).to_xarray()  # Located in Indian Ocean
ds_points2 = argo_loader.profile(2900737, 3).to_xarray()  # Located in Pacific Ocean
ds_points3 = argo_loader.profile(3900267, 3).to_xarray()  # Located in South Atlantic
ds_points4 = argo_loader.profile(3901629, 2).to_xarray()  # Located in North Atlantic

# Steps taken to convert ds_points which are in the form of xarray.
# For more information refer to the final report.
ds1 = ds_points1.argo.point2profile()
ds2 = ds_points2.argo.point2profile()
ds3 = ds_points3.argo.point2profile()
ds4 = ds_points4.argo.point2profile()
df1 = ds1.to_dataframe()
df2 = ds2.to_dataframe()
df3 = ds3.to_dataframe()
df4 = ds4.to_dataframe()

# 1- Incorporating the N-Level index (a the by-product of the above steps), as columns
# 2- Only keeping the useful columns for the purposes of this projection
# 3- All details in the report.
df1 = df1.reset_index(level='N_LEVELS') [['N_LEVELS','PRES','PSAL','TEMP','LONGITUDE','LATITUDE']]
df2 = df2.reset_index(level='N_LEVELS') [['N_LEVELS','PRES','PSAL','TEMP','LONGITUDE','LATITUDE']]
df3 = df3.reset_index(level='N_LEVELS') [['N_LEVELS','PRES','PSAL','TEMP','LONGITUDE','LATITUDE']]
df4 = df4.reset_index(level='N_LEVELS') [['N_LEVELS','PRES','PSAL','TEMP','LONGITUDE','LATITUDE']]
dfs = [df1, df2, df3, df4]

# Saving the mean locations of the selected argos, to plot on the map
location1 = (df1["LONGITUDE"].mean(), df1["LATITUDE"].mean())
location2 = (df2["LONGITUDE"].mean(), df2["LATITUDE"].mean())
location3= (df3["LONGITUDE"].mean(), df3["LATITUDE"].mean())
location4 = (df4["LONGITUDE"].mean(), df4["LATITUDE"].mean())
locations = [location1, location2, location3, location4]


# Perparing the world map
fig = plt.figure(figsize=(15, 15))
m = Basemap(projection='cyl', resolution='i', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180)
m.etopo(scale=0.5, alpha=0.5)

color_list = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

# Pinpointing the argo locations on the map
for count, location in enumerate(locations):
    x, y = m(location[0], location[1])
    plt.plot(x, y, 'x', markersize = 15, mew = 3, color = color_list[count])

plt.savefig("map_of_locations.png")

# Plotting a customized correlation plot. Details in the report.
for count, df in enumerate(dfs):
    df.drop(['LONGITUDE', 'LATITUDE'], axis=1, inplace=True)
    g = sns.PairGrid(df)
    g.map_diag(sns.histplot, color = color_list[count])
    g.map_lower(sns.scatterplot, alpha=0.4, color = color_list[count])
    g.map_upper(reg_coef, color = color_list[count])
    g.savefig(f'correlation{count + 1}.png')