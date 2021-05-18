import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# sns.set_theme(style="darkgrid")

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

# Seaborn plots for diarrhoea