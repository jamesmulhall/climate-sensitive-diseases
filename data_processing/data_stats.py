import pandas as pd
from scipy import stats
from scikit_posthocs import posthoc_dunn

# Read in data
vietnam = pd.read_excel("C:\\Users\\james\\OneDrive\\Documents\\Vietnam_Project\\climate-sensitive-diseases-private\\full_data_fixed.xlsx")

# Add subregion column to dataset
def label_subregion(row):
    if row['province'] in ['Lai Châu', 'Sơn La', 'Điện Biên']:
        return "north_west"
    if row['province'] in ['Lào Cai', 'Yên Bái', 'Hòa Bình', 'Hà Giang', 'Tuyên Quang', 'Phú Thọ', 'Cao Bằng', 'Lạng Sơn', 'Bắc Cạn', 'Thái Nguyên', 'Quảng Ninh']:
        return "north_east"
    if row['province'] in ['Phú Thọ', 'Vĩnh Phúc', 'Bắc Giang', 'Hà Nội', 'Hải Phòng', 'Hải Dương', 'Hưng Yên', 'Nam Định', 'Thái Bình', 'Ninh Bình']:
        return "north_delta"
    if row['province'] in ['Thanh Hóa', 'Nghệ An', 'Hà Tính', 'Quảng Bình', 'Quảng Trị']:
        return "north_central"
    if row['province'] in ['Đà Nẵng', 'Quảng Nam', 'Quảng Ngãi', 'Bình Định', 'Phú Yên', 'Khánh Hòa', 'Ninh Thuận', 'Bình Thuận']:
        return "south_central"
    if row['province'] in ['Kon Tum', 'Gia Lai', 'Đắk Lắk', 'Đắc Nông', 'Lâm Đồng']:
        return "central_highlands"
    if row['province'] in ['Cà Mau', 'Bạc Liêu', 'Kiên Giang', 'Sóc Trăng', 'Cần Thơ', 'An Giang', 'Trà Vinh', 'Đồng Tháp', 'Tiền Giang', 'Long An', 'BR Vũng Tàu', 'Tây Ninh', 'Bình Phước']:
        return "south"

# Add region column to dataset
def label_region(row):
    if row['subregion'] in ['north_west', 'north_east', 'north_delta']:
        return "North"
    if row['subregion'] in ['north_central', 'south_central', 'central_highalnds']:
        return "Central"
    if row['subregion'] in ['south']:
        return "South"

vietnam["subregion"] = vietnam.apply(label_subregion, axis = 1)
vietnam["Region"] = vietnam.apply(label_region, axis=1)


# Test normality by iterating through numeric columns
normal_results = pd.DataFrame(columns=["variable", "shapiro_statistic", "p-value"])

for col in vietnam.iloc[:, 3:21]:
    shapiro_test = stats.shapiro(vietnam[col].dropna())
    print(col, shapiro_test.pvalue)
    res = pd.DataFrame({"variable": col, "shapiro_statistic": shapiro_test.statistic, "p-value": shapiro_test.pvalue}, index=[0])
    normal_results = normal_results.append(res, ignore_index=True)

normal_results.to_excel("C:\\Users\\james\\OneDrive\\Documents\\Vietnam_Project\\shapiro_results.xlsx")


# Get summary stats on variables per region
vietnam[vietnam["Region"] == "North"]["Dengue_fever_rates"].describe()
vietnam[vietnam["Region"] == "Central"]["Dengue_fever_rates"].describe()
vietnam[vietnam["Region"] == "South"]["Dengue_fever_rates"].describe()

vietnam[vietnam["Region"] == "North"]["Diarrhoea_rates"].describe()
vietnam[vietnam["Region"] == "Central"]["Diarrhoea_rates"].describe()
vietnam[vietnam["Region"] == "South"]["Diarrhoea_rates"].describe()

vietnam[vietnam["Region"] == "North"]["Average_Humidity"].describe()
vietnam[vietnam["Region"] == "Central"]["Average_Humidity"].describe()
vietnam[vietnam["Region"] == "South"]["Average_Humidity"].describe()

vietnam[vietnam["Region"] == "North"]["Average_temperature"].describe()
vietnam[vietnam["Region"] == "Central"]["Average_temperature"].describe()
vietnam[vietnam["Region"] == "South"]["Average_temperature"].describe()

vietnam[vietnam["Region"] == "North"]["Total_Evaporation"].describe()
vietnam[vietnam["Region"] == "Central"]["Total_Evaporation"].describe()
vietnam[vietnam["Region"] == "South"]["Total_Evaporation"].describe()

vietnam[vietnam["Region"] == "North"]["n_hours_sunshine"].describe()
vietnam[vietnam["Region"] == "Central"]["n_hours_sunshine"].describe()
vietnam[vietnam["Region"] == "South"]["n_hours_sunshine"].describe()

vietnam[vietnam["Region"] == "North"]["Total_Rainfall"].describe()
vietnam[vietnam["Region"] == "Central"]["Total_Rainfall"].describe()
vietnam[vietnam["Region"] == "South"]["Total_Rainfall"].describe()


# Create dataframes to store statistical test results in
kruskal_results = pd.DataFrame()
dunn_results = pd.DataFrame()

# DF kruskal test
dengue_kruskal = stats.kruskal(vietnam[vietnam["Region"] == "North"]["Dengue_fever_rates"].dropna(), vietnam[vietnam["Region"] == "Central"]["Dengue_fever_rates"].dropna(), vietnam[vietnam["Region"] == "South"]["Dengue_fever_rates"].dropna())
kruskal_results = kruskal_results.append({"Variable": 'DF', "Statistic": dengue_kruskal.statistic, "p-value": dengue_kruskal.pvalue}, ignore_index=True)

# DF post-hoc test
dengue_post = posthoc_dunn(vietnam.dropna(), val_col='Dengue_fever_rates', group_col='Region')
dengue_post["Variable"] = 'DF'
dunn_results = dunn_results.append(dengue_post)

# Diarrhoea kruskal test
diarrhoea_kruskal = stats.kruskal(vietnam[vietnam["Region"] == "North"]["Diarrhoea_rates"].dropna(), vietnam[vietnam["Region"] == "Central"]["Diarrhoea_rates"].dropna(), vietnam[vietnam["Region"] == "South"]["Diarrhoea_rates"].dropna())
kruskal_results = kruskal_results.append({"Variable": 'Diarrhoea', "Statistic": diarrhoea_kruskal.statistic, "p-value": diarrhoea_kruskal.pvalue}, ignore_index=True)

# Diarrhoea post-hoc test
diarrhoea_post = posthoc_dunn(vietnam.dropna(), val_col='Diarrhoea_rates', group_col='Region')
diarrhoea_post["Variable"] = 'Diarrhoea_rates'
dunn_results = dunn_results.append(diarrhoea_post)

# Total rainfall kruskal test
rain_kruskal = stats.kruskal(vietnam[vietnam["Region"] == "North"]["Total_Rainfall"].dropna(), vietnam[vietnam["Region"] == "Central"]["Total_Rainfall"].dropna(), vietnam[vietnam["Region"] == "South"]["Total_Rainfall"].dropna())
kruskal_results = kruskal_results.append({"Variable": 'Total_Rainfall', "Statistic": rain_kruskal.statistic, "p-value": rain_kruskal.pvalue}, ignore_index=True)

# Average temperature kruskal test
temp_kruskal = stats.kruskal(vietnam[vietnam["Region"] == "North"]["Average_temperature"].dropna(), vietnam[vietnam["Region"] == "Central"]["Average_temperature"].dropna(), vietnam[vietnam["Region"] == "South"]["Average_temperature"].dropna())
kruskal_results = kruskal_results.append({"Variable": 'Average_temperature', "Statistic": temp_kruskal.statistic, "p-value": temp_kruskal.pvalue}, ignore_index=True)

# Average temperature post-hoc test
temp_post = posthoc_dunn(vietnam.dropna(), val_col='Average_temperature', group_col='Region')
temp_post["Variable"] = 'Average_temperature'
dunn_results = dunn_results.append(temp_post)

# Average humidity kruskal test
humid_kruskal = stats.kruskal(vietnam[vietnam["Region"] == "North"]["Average_Humidity"].dropna(), vietnam[vietnam["Region"] == "Central"]["Average_Humidity"].dropna(), vietnam[vietnam["Region"] == "South"]["Average_Humidity"].dropna())
kruskal_results = kruskal_results.append({"Variable": 'Average_Humidity', "Statistic": humid_kruskal.statistic, "p-value": humid_kruskal.pvalue}, ignore_index=True)

# Average humidity post-hoc test
humid_post = posthoc_dunn(vietnam.dropna(), val_col='Average_Humidity', group_col='Region')
humid_post["Variable"] = 'Average_Humidity'
dunn_results = dunn_results.append(humid_post)

# Total evaporation kruskal test
evap_kruskal = stats.kruskal(vietnam[vietnam["Region"] == "North"]["Total_Evaporation"].dropna(), vietnam[vietnam["Region"] == "Central"]["Total_Evaporation"].dropna(), vietnam[vietnam["Region"] == "South"]["Total_Evaporation"].dropna())
kruskal_results = kruskal_results.append({"Variable": 'Total_Evaporation', "Statistic": evap_kruskal.statistic, "p-value": evap_kruskal.pvalue}, ignore_index=True)

# Total evaporation post-hoc test
evap_post = posthoc_dunn(vietnam.dropna(), val_col='Total_Evaporation', group_col='Region')
evap_post["Variable"] = 'Total_Evaporation'
dunn_results = dunn_results.append(evap_post)

# n_hours_sunshine kruskal test
sun_kruskal = stats.kruskal(vietnam[vietnam["Region"] == "North"]["n_hours_sunshine"].dropna(), vietnam[vietnam["Region"] == "Central"]["n_hours_sunshine"].dropna(), vietnam[vietnam["Region"] == "South"]["n_hours_sunshine"].dropna())
kruskal_results = kruskal_results.append({"Variable": 'n_hours_sunshine', "Statistic": sun_kruskal.statistic, "p-value": sun_kruskal.pvalue}, ignore_index=True)

# n_hours_sunshine post-hoc test
sun_post = posthoc_dunn(vietnam.dropna(), val_col='n_hours_sunshine', group_col='Region')
sun_post["Variable"] = 'n_hours_sunshine'
dunn_results = dunn_results.append(sun_post)

# Save results
kruskal_results.to_excel("C:\\Users\\james\\OneDrive\\Documents\\Vietnam_Project\\kruskal_results.xlsx")
dunn_results.to_excel("C:\\Users\\james\\OneDrive\\Documents\\Vietnam_Project\\dunn_results.xlsx")
