
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
# import fiona # fiona package is only used if you need to check the layer names, otherwise it is not required

#  pull data from the COVID API
df = pd.read_csv('https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=newCasesBySpecimenDateRollingRate&format=csv')
df['date'] = pd.to_datetime(df['date'])
df = df.rename(columns={"areaCode": "Lacode"})

# keep latest date for shading the map
maxdate = max(df['date'])
df = df[(df['date']==maxdate)]

# Hex map data from the gpkg from here https://github.com/houseofcommonslibrary/uk-hex-cartograms-noncontiguous
gpkg = 'C:/Users/Administrator/Documents/GitHub/hex-map-example/geopackages/LocalAuthorities-lowertier.gpkg'

# Check the layer names. These are used to extract each map layer and sometimes change from those referenced below. Uncomment the statements below to check the names if needed.
# for layername in fiona.listlayers(gpkg):
#     print(layername) 

# Pull the layer information from the geopackage
ltla_hex = gpd.read_file(gpkg, layer='4 LTLA-2019')
labels = gpd.read_file(gpkg, layer='1 Group labels')
background = gpd.read_file(gpkg, layer='7 Background')

# Merge the case data to the hex map
ltla_hex_data = ltla_hex.merge(df,on='Lacode',how='left')

# Make a plot of the LTLAs colored by the number of cases
fig, ax = plt.subplots(figsize=(10,13),dpi=(600))

# set the background colour for the UK map
background.plot(ax=ax,alpha=0.3, color='xkcd:light grey')

# plot the values, in this example 7 day COVID case rates per 100k population
ltla_hex_data.plot(ax=ax,column='newCasesBySpecimenDateRollingRate', legend=True)

# add labels to each area
for x in range(0,len(labels)):
    plt.text(labels['geometry'][x].x,labels['geometry'][x].y-0.25,labels['Group-labe'][x],horizontalalignment=labels['LabelPosit'][x].lower(),fontsize=6,color='white')

# Remove the axes
ax.get_xaxis().set_visible(False)  
ax.get_yaxis().set_visible(False) 

# set the image background colour
ax.set_facecolor('xkcd:dark grey')

# display and save the image
plt.show()
fig.savefig("C:/Users/Administrator/Documents/GitHub/hex-map-example/out/hex-map-example-output.png")