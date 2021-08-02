import geopandas as gp
import pandas as pd 
import matplotlib.pyplot as plt
import contextily as ctx

# Read in json of Vietnam and climate/disease data
geo_data = gp.read_file("C:\\Users\\james\\OneDrive\\Documents\\Vietnam_Project\\climate-sensitive-diseases-private\\vietnam.json")
climate_data = pd.read_excel("C:\\Users\\james\\OneDrive\\Documents\\Vietnam_Project\\climate-sensitive-diseases-private\\Final_full_cleaned_dataset.xlsx")

# Rename so both dataframes have a province column to merge on
geo_data = geo_data.rename(columns={'name':'province'})

# View which provinces are not in the other dataset
for x in geo_data['province'].unique():
    if not sum(x == y for y in climate_data['province'].unique()):
        print(x)

for x in climate_data['province'].unique():
    if not sum(x == y for y in geo_data['province'].unique()):
        print(x)

# Match province names before merge
geo_data['province'].replace("Bà Rịa - Vũng Tàu", "BR Vũng Tàu", inplace = True)
geo_data['province'].replace("Hà Tĩnh", "Hà Tính", inplace = True)
geo_data['province'].replace("Bắc Kạn", "Bắc Cạn", inplace = True)
geo_data['province'].replace("Thừa Thiên - Huế", "TT Huế", inplace = True)
geo_data['province'].replace("Đăk Nông", "Đắc Nông", inplace = True)

# Merge and convert to Web Mercator to allow adding of Web Mercator basemap
full_data = geo_data.merge(climate_data, on='province', how='left')
full_data = full_data.to_crs(epsg=3857)

# Check max value
# max(full_data.groupby('province')['Diarrhoea_rates'].median())
max(full_data.groupby('province')['Diarrhoea_rates'].mean())

# Add mean rates for each province
full_data['mean_diarrhoea_rates'] = full_data['Diarrhoea_rates'].groupby(full_data['province']).transform('mean')

# Plot with CartoDB basemap
# optionally manually set vmax and vmin if different colour scale is desired
fig, ax = plt.subplots()
fig = full_data.plot(column='mean_diarrhoea_rates', 
                     cmap='OrRd', 
                     legend=True, 
                     legend_kwds={'label': 'Mean Monthly Diarrhoea Rates per 100k Population'},
                     missing_kwds={"color": "whitesmoke", 
                                   "facecolor": "none", 
                                   "edgecolor": "gainsboro",
                                   "hatch": "///",
                                   "label":"Missing values"}
                    )
plt.xlabel("Latitude (m)")
plt.ylabel("Longitude (m)")
ctx.add_basemap(fig, source=ctx.providers.CartoDB.PositronNoLabels)
#ctx.add_basemap(fig, source=ctx.providers.CartoDB.VoyagerOnlyLabels)
plt.savefig("C:\\Users\\james\\OneDrive\\Documents\\Vietnam_Project\\Figures\\diarrhoea_rates_map.png", dpi=600)
plt.show()

# Missing rates data
full_data[full_data['province'] == "TT Huế"]
climate_data[climate_data['province'] == "TT Huế"]

# Mapping options
ctx.providers.OpenStreetMap.keys()
ctx.providers.CartoDB.keys()