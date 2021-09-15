import pandas as pd 
import matplotlib.pyplot as plt

# Read in json of Vietnam and climate/disease data
pop_data = pd.read_excel("C:\\Users\\james\\OneDrive\\Documents\\Vietnam_Project\\climate-sensitive-diseases-private\\province_populations.xlsx")
climate_data = pd.read_excel("C:\\Users\\james\\OneDrive\\Documents\\Vietnam_Project\\climate-sensitive-diseases-private\\Final_full_cleaned_dataset.xlsx")

# Rename so both dataframes have a province column to merge on
pop_data = pop_data.melt(id_vars=["province"], 
                         var_name="year", 
                         value_name="population")

pop_data['population'] = pop_data['population'] * 1000

# View which provinces are not in the other dataset
for x in pop_data['province'].unique():
    if not sum(x == y for y in climate_data['province'].unique()):
        print(x)

for x in climate_data['province'].unique():
    if not sum(x == y for y in pop_data['province'].unique()):
        print(x)

# Match province names before merge
pop_data['province'].replace("Bà Rịa - Vũng Tàu", "BR Vũng Tàu", inplace = True)
pop_data['province'].replace("Hà Tĩnh", "Hà Tính", inplace = True)
pop_data['province'].replace("Bắc Kạn", "Bắc Cạn", inplace = True)
pop_data['province'].replace("Hoà Bình", "Hòa Bình", inplace = True)
pop_data['province'].replace("Khánh Hoà", "Khánh Hòa", inplace = True)
pop_data['province'].replace("Lâm Ðồng", "Lâm Đồng", inplace = True)
pop_data['province'].replace("Nam Ðịnh", "Nam Định", inplace = True)
pop_data['province'].replace("Thừa Thiên Huế", "TT Huế", inplace = True)
pop_data['province'].replace("Thanh Hoá", "Thanh Hóa", inplace = True)
pop_data['province'].replace("Ðiện Biên", "Điện Biên", inplace = True)
pop_data['province'].replace("Ðà Nẵng", "Đà Nẵng", inplace = True)
pop_data['province'].replace("Ðắk Nông", "Đắc Nông", inplace = True)
pop_data['province'].replace("Ðắk Lắk", "Đắk Lắk", inplace = True)
pop_data['province'].replace("Ðồng Tháp", "Đồng Tháp", inplace = True)
pop_data['province'].replace("Bình Ðịnh", "Bình Định", inplace = True)

# No more provinces left from climate and case data
for x in climate_data['province'].unique():
    if not sum(x == y for y in pop_data['province'].unique()):
        print(x)

climate_data['year'] = climate_data['year_month'].dt.year

# Convert year from object to int
pop_data['year'] = pop_data['year'].astype(str).astype(int)

# Merge
full_data = pd.merge(climate_data, pop_data, on=['province', 'year'], how='left')

# Calculate rates
full_data['Influenza_rates'] = (full_data['Influenza_cases'] / full_data['population']) * 100000
full_data['Dengue_fever_rates'] = (full_data['Dengue_fever_cases'] / full_data['population']) * 100000
full_data['Diarrhoea_rates'] = (full_data['Diarrhoea_cases'] / full_data['population']) * 100000

full_data.drop(columns=['Unnamed: 0', 'year', 'population'], inplace=True)

# Save
full_data.to_excel("C:\\Users\\james\\OneDrive\\Documents\\Vietnam_Project\\climate-sensitive-diseases-private\\full_data_fixed2.xlsx")