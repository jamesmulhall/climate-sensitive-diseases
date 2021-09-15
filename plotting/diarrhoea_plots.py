import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")

# Read in data
vietnam = pd.read_excel("C:\\Users\\james\\OneDrive\\Documents\\Vietnam_Project\\climate-sensitive-diseases-private\\full_data_fixed.xlsx")

# Divide data into subregions
vietnam.province.unique()
north_west = vietnam.loc[vietnam["province"].isin(['Lai Châu', 'Sơn La', 'Điện Biên'])]
north_east = vietnam.loc[vietnam["province"].isin(['Lào Cai', 'Yên Bái', 'Hòa Bình', 'Hà Giang', 'Tuyên Quang', 'Phú Thọ', 'Cao Bằng', 'Lạng Sơn', 'Bắc Cạn', 'Thái Nguyên', 'Quảng Ninh'])]
north_delta = vietnam.loc[vietnam["province"].isin(['Phú Thọ', 'Vĩnh Phúc', 'Bắc Giang', 'Hà Nội', 'Hải Phòng', 'Hải Dương', 'Hưng Yên', 'Nam Định', 'Thái Bình', 'Ninh Bình'])] # no Bac Ninh or Ha Nam
north_central = vietnam.loc[vietnam["province"].isin(['Thanh Hóa', 'Nghệ An', 'Hà Tính', 'Quảng Bình', 'Quảng Trị'])] # no Thua Thien
south_central = vietnam.loc[vietnam["province"].isin(['Đà Nẵng', 'Quảng Nam', 'Quảng Ngãi', 'Bình Định', 'Phú Yên', 'Khánh Hòa', 'Ninh Thuận', 'Bình Thuận'])]
central_highlands = vietnam.loc[vietnam["province"].isin(['Kon Tum', 'Gia Lai', 'Đắk Lắk', 'Đắc Nông', 'Lâm Đồng'])]
south = vietnam.loc[vietnam["province"].isin(['Cà Mau', 'Bạc Liêu', 'Kiên Giang', 'Sóc Trăng', 'Cần Thơ', 'An Giang', 'Trà Vinh', 'Đồng Tháp', 'Tiền Giang', 'Long An', 'BR Vũng Tàu', 'Tây Ninh', 'Bình Phước'])] #no Hau Giang, Vinh Long, Ben Tre, Ho Chi Minh, Dong Nai

# Alternatively, add subregion column to full dataset
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

def label_region(row):
    if row['subregion'] in ['north_west', 'north_east', 'north_delta']:
        return "North"
    if row['subregion'] in ['north_central', 'south_central', 'central_highalnds']:
        return "Central"
    if row['subregion'] in ['south']:
        return "South"

vietnam["region"] = vietnam.apply(label_subregion, axis = 1)

# Plot diarrhoea rates per province
g = sns.catplot(x = "province", y = "Diarrhoea_rates", data = vietnam.dropna(subset = ["Diarrhoea_rates"]), kind = "box")
g.set(xlabel = "Province", ylabel = "Monthly Diarrhoea Rates per 100k Population")
plt.xticks(rotation=90)
plt.tight_layout()
#plt.savefig("C:\\Users\\james\\OneDrive\\Documents\\Vietnam_Project\\Figures\\diarrhoea_rates.svg")
plt.show()

# Plot dengue fever rates per province (symlog scale)
g = sns.catplot(x = "province", y = "Dengue_fever_rates", data = vietnam.dropna(subset = ["Dengue_fever_rates"]), kind = "box", whis=1.5)
g.set(xlabel = "Province", ylabel = "Monthly Symlog Dengue Fever Rates per 100k Population", yscale='symlog', ylim=(-0.15, 100))
plt.xticks(rotation=90)
plt.tight_layout()
#plt.savefig("C:\\Users\\james\\OneDrive\\Documents\\Vietnam_Project\\Figures\\diarrhoea_rates.svg")
plt.show()

# Plot diarrhoea rates per province (log scale)
g = sns.catplot(x = "province", y = "Diarrhoea_rates", data = vietnam.dropna(subset = ["Diarrhoea_rates"]), kind = "box")
g.set(xlabel = "Province", ylabel = "Diarrhoea Rates per 100k Population (Log Scale)", title = "Diarrhoea Rates in Vietnam by Province", yscale = "log")
plt.xticks(rotation=90)
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
        df_lag = df_lag.groupby("province", group_keys = False).apply(lambda group: group.iloc[:-1, :]) # drop values shifted into incorrect provinces
    return df_lag

def concat_lags(df, colname, lag):
    """"Adds lags by adding new rows to dataframe. 'Lag' column is added to specify number of lag months."""
    df_lag = df.copy()
    df_lag = df_lag.sort_values(["province", "year_month"]) # order by province and date to make sure shift is correct
    df_lag["Lag"] = 0
    df_list = [df_lag]
    for i in range(1, lag + 1):
        df_lag[colname] = df_lag[colname].shift(-1)
        df_lag = df_lag.groupby("province", group_keys = False).apply(lambda group: group.iloc[:-1, :])
        df_lag["Lag"] = i
        df_list.append(df_lag)
    return pd.concat(df_list)

diarrhoea_lags = add_lags(vietnam, 'Diarrhoea_rates', 6)
diarrhoea_lags

concat_diarrhoea_lags = concat_lags(vietnam, "Diarrhoea_rates", 6)
concat_diarrhoea_lags.loc[concat_diarrhoea_lags['Lag'] == 6]


# Full heatmap of lag correlations in Vietnam
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

corr_matrix = diarrhoea_lags.corr(method = "spearman")
g = sns.heatmap(corr_matrix, cmap="PiYG", center = 0)
g.set(title = "Spearman Correlations in Vietnam")
plt.show()

# Full heatmap for Thai Binh
thai_binh_lags = add_lags(vietnam[vietnam['province'] == 'Thái Bình'], "Diarrhoea_rates", 6)
corr_matrix = thai_binh_lags.corr(method = "spearman")
g = sns.heatmap(corr_matrix, cmap="PiYG", center = 0)
g.set(title = "Spearman Correlations in Thai Binh")
plt.tight_layout()
plt.show()

# KDE plots between min temp and same month cases, showing different regions
g = sns.FacetGrid(diarrhoea_lags, col = "region", col_wrap = 4)
g.map(sns.kdeplot, "Min_Absolute_Temperature", "Diarrhoea_rates", fill = True, cmap = "crest")
plt.show()

# KDE plots between max abs temp and cases 1 month later, showing different regions
g = sns.FacetGrid(diarrhoea_lags, col = "region", col_wrap = 4)
g.map(sns.kdeplot, "Max_Absolute_Temperature", "Lag_1_Diarrhoea_rates", fill = True, cmap = "crest")
g.set(xlabel = "Max Absolute Temperature (°C)", ylabel = "Diarrhoea Rates (1 Mo. Lag)")
plt.suptitle("Correlations between Temperature and Diarrhoea in Vietnam")
plt.show()

# KDE plots between min temp and lagged cases 2 month later, showing different regions
g = sns.FacetGrid(diarrhoea_lags, col = "region", col_wrap = 4)
g.map(sns.kdeplot, "Min_Absolute_Temperature", "Lag_2_Diarrhoea_rates", fill = True, cmap = "crest")
plt.show()

# KDE plots between min temp and lagged cases 3 month later, showing different regions
g = sns.FacetGrid(diarrhoea_lags, col = "region", col_wrap = 4)
g.map(sns.kdeplot, "Min_Absolute_Temperature", "Lag_3_Diarrhoea_rates", fill = True, cmap = "crest")
plt.show()

# KDE plot between min temp and lagged cases, showing different lags for 1 region
highlands_concat_diarrhoea = concat_lags(central_highlands, "Diarrhoea_rates", 5)

g = sns.FacetGrid(highlands_concat_diarrhoea, col = "Lag", col_wrap = 3)
g.map(sns.kdeplot, "Min_Absolute_Temperature", "Diarrhoea_rates", fill = True, cmap = "crest")
plt.show()

# Regression plots
g = sns.lmplot(x = "Total_Rainfall", y = "Diarrhoea_rates", col = "Lag", col_wrap = 3, line_kws = {'color':'cyan'}, data = highlands_concat_diarrhoea)
plt.show()

g = sns.lmplot(x = "Total_Rainfall", y = "Diarrhoea_rates", col = "Lag", col_wrap = 3, line_kws = {'color':'cyan'}, data = highlands_concat_diarrhoea, lowess = True)
plt.show()

# Single Province
dien_bien_concat = concat_lags(vietnam.loc[vietnam["province"] == "Điện Biên"], "Diarrhoea_rates", 5)
g = sns.lmplot(x = "n_raining_days", y = "Diarrhoea_rates", col = "Lag", col_wrap = 3, line_kws = {'color':'turquoise'}, data = dien_bien_concat, lowess = False)
plt.show()