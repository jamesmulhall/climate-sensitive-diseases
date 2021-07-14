import pandas as pd

vietnam = pd.read_excel("C:\\Users\\james\\OneDrive\\Documents\\Vietnam_Project\\climate-sensitive-diseases\\Final_full_cleaned_dataset.xlsx")
vietnam["province"].replace("Điện Biên", "Dien Bien", inplace = True)
vietnam["province"].unique()

vietnam.head(5)
vietnam["Influenza_rates"] = vietnam["Influenza_rates"] / 10
vietnam["Dengue_fever_rates"] = vietnam["Dengue_fever_rates"] / 10
vietnam["Diarrhoea_rates"] = vietnam["Diarrhoea_rates"] / 10
vietnam.head(5)

vietnam.to_excel("C:\\Users\\james\\OneDrive\\Documents\\Vietnam_Project\\100k_anglicised.xlsx")
