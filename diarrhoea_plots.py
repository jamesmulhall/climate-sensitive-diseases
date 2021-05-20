import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")

vietnam = pd.read_excel("C:\\Users\\james\\OneDrive\\Documents\\Vietnam_Project\\climate-sensitive-diseases\\Final_full_cleaned_dataset.xlsx")
print(vietnam.info())
print(vietnam.head(5))

# Divide data into subregions
vietnam.province.unique()
north_west = vietnam.loc[vietnam["province"].isin(['Lai Châu', 'Sơn La', 'Điện Biên'])]
north_east = vietnam.loc[vietnam["province"].isin(['Lào Cai', 'Yên Bái', 'Hòa Bình', 'Hà Giang', 'Tuyên Quang', 'Phú Thọ', 'Cao Bằng', 'Lạng Sơn', 'Bắc Cạn', 'Thái Nguyên', 'Quảng Ninh'])]
north_delta = vietnam.loc[vietnam["province"].isin(['Phú Thọ', 'Vĩnh Phúc', 'Bắc Giang', 'Hà Nội', 'Hải Phòng', 'Hải Dương', 'Hưng Yên', 'Nam Định', 'Thái Bình', 'Ninh Bình'])] # no Bac Ninh or Ha Nam
north_central = vietnam.loc[vietnam["province"].isin(['Thanh Hóa', 'Nghệ An', 'Hà Tính', 'Quảng Bình', 'Quảng Trị'])] # no Thua Thien
south_central = vietnam.loc[vietnam["province"].isin(['Đà Nẵng', 'Quảng Nam', 'Quảng Ngãi', 'Bình Định', 'Phú Yên', 'Khánh Hòa', 'Ninh Thuận', 'Bình Thuận'])]
central_highlands = vietnam.loc[vietnam["province"].isin(['Kon Tum', 'Gia Lai', 'Đắk Lắk', 'Đắc Nông', 'Lâm Đồng'])]
south = vietnam.loc[vietnam["province"].isin(['Cà Mau', 'Bạc Liêu', 'Kiên Giang', 'Sóc Trăng', 'Cần Thơ', 'An Giang', 'Trà Vinh', 'Đồng Tháp', 'Tiền Giang', 'Long An', 'BR Vũng Tàu', 'Tây Ninh', 'Bình Phước'])] #no Hau Giang, Vinh Long, Ben Tre, Ho Chi Minh, Dong Nai
# Double check those

# Alternatively, add subregion column
def label_region (row):
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

vietnam.apply(label_region, axis = 1) # check results
vietnam["region"] = vietnam.apply(label_region, axis = 1)

# Seaborn plots for diarrhoea
sns.relplot(x = "Average_temperature", y = "Diarrhoea_rates", data = vietnam)
plt.show()

sns.relplot(x = "Total_Rainfall", y = "Diarrhoea_rates", data = central_highlands)
plt.show()


# Lag function
def add_lags(df, colname, lag):
    """
    Adds new columns to dataframe for lagging a variable forward in time up to [lag] months.
    Lag_1_colname refers to the value for colname 1 month later.
    """
    df_lag = df.copy()
    df_lag = df_lag.sort_values(["province", "year_month"]) # order by province and date to make sure shift is correct
    for i in range(1, lag + 1):
        df_lag['Lag_' + str(i) + '_' + colname] = df_lag[colname].shift(-i)
        df_lag = df_lag.groupby("province", group_keys = False).apply(lambda group: group.iloc[1:, :]) # drop values shifted into incorrect provinces
    return df_lag

# def concat_lags(df, colname, lag, dropna = False):
#     res = df.copy()
#     df_lag = df.copy()
#     for i range(1, lag + 1):
#         df_lag.rename({colname: 'Lag_' + str(i) + '_' + colname})
#         df['Lag_' + str(i) + '_' + colname].shift(i)
#         res = res.concat #will reset keys, need to fix later

diarrhoea_lags = add_lags(vietnam, 'Diarrhoea_rates', 6)
diarrhoea_lags

# Full heatmap of lag correlations in Vietnam
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

corr_matrix = diarrhoea_lags.corr(method = "spearman")
sns.heatmap(corr_matrix, cmap="PiYG", center = 0)
plt.show()

# Correlation between min temp and lagged cases, showing different provinces
g = sns.FacetGrid(diarrhoea_lags, col = "region", col_wrap = 4)
g.map(sns.kdeplot, "Min_Absolute_Temperature", "Diarrhoea_rates", fill = True, cmap = "crest")
plt.show()

g = sns.FacetGrid(diarrhoea_lags, col = "region", col_wrap = 4)
g.map(sns.kdeplot, "Min_Absolute_Temperature", "Lag_1_Diarrhoea_rates", fill = True, cmap = "crest")
plt.show()

g = sns.FacetGrid(diarrhoea_lags, col = "region", col_wrap = 4)
g.map(sns.kdeplot, "Min_Absolute_Temperature", "Lag_2_Diarrhoea_rates", fill = True, cmap = "crest")
plt.show()

g = sns.FacetGrid(diarrhoea_lags, col = "region", col_wrap = 4)
g.map(sns.kdeplot, "Min_Absolute_Temperature", "Lag_3_Diarrhoea_rates", fill = True, cmap = "crest")
plt.show()

# Correlation between min temp and lagged cases, showing different lags for 1 province (coming soon?)


# Mess
cols = [19, 21, 22, 23, 24, 25]
lag1 = diarrhoea_lags.drop(diarrhoea_lags.columns[cols], axis = 1)

cols2 = [19, 20, 22, 23, 24, 25]
lag2 = diarrhoea_lags.drop(diarrhoea_lags.columns[cols2], axis = 1)

cols3 = [19, 20, 21, 23, 24, 25]
lag3 = diarrhoea_lags.drop(diarrhoea_lags.columns[cols3], axis = 1)

cols4 = [19, 20, 21, 22, 24, 25]
lag4 = diarrhoea_lags.drop(diarrhoea_lags.columns[cols4], axis = 1)

cols5 = [19, 20, 21, 22, 23, 25]
lag5 = diarrhoea_lags.drop(diarrhoea_lags.columns[cols5], axis = 1)

cols6 = [19, 20, 21, 22, 23, 24]
lag6 = diarrhoea_lags.drop(diarrhoea_lags.columns[cols6], axis = 1)

for i in [lag1, lag2, lag3, lag4, lag5, lag6]:
    i.rename(columns = {i.columns[19]: "Diarrhoea_rates"}, inplace = True)

lag_list = [vietnam, lag1, lag2, lag3, lag4, lag5, lag6]
diarrhoea_concat = pd.concat(lag_list, keys = ['lag0','lag1','lag2','lag3','lag4','lag5','lag6'])
diarrhoea_concat['lag'] = diarrhoea_concat.index.get_level_values(0)


sns.displot(north_central, x = "Average_temperature", y = "Diarrhoea_rates", kind = "kde", fill = True)
plt.show()
sns.displot(lag1, x = "Average_temperature", y = "Diarrhoea_rates", kind = "kde", fill = True)
plt.show()


# sns.displot(diarrhoea_concat, x = "Average_temperature", y = "Diarrhoea_rates", kind = "kde", hue = "lag", fill = True)
sns.displot(diarrhoea_concat, x = "lag", y = "Average_temperature", kind = "kde", fill = True)
plt.show()

sns.displot(diarrhoea_concat, x = 'Diarrhoea_rates', binwidth = 200)
plt.show()

bins = [0, 1, 5, 10, 25, 50, 100]
labels = [1,2,3,4,5,6]
df['binned'] = pd.cut(df['percentage'], bins=bins, labels=labels)
print (df)

sns.displot(diarrhoea_concat, x = 'lag', y = 'Average_temperature', hue = "Diarrhoea_rates")
plt.show()

sns.displot(vietnam, )