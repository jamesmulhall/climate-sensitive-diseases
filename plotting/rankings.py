import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Dengue Fever

# Plot style
plt.rcParams['figure.figsize'] = [20.0, 7.0]
plt.rcParams['font.size'] = 16
matplotlib.rcParams.update({'font.size': 25})
sns.set_style('whitegrid')
sns.set_context("notebook", 1.4)

# Set up plot grid
fig = plt.figure()
AX = gridspec.GridSpec(2,6, bottom=0.2, wspace=0.5)
ax1  = plt.subplot(AX[:,0:3])
ax2 = plt.subplot(AX[:,3:6])

# Read in data and calculate mean rankings
df = pd.read_excel("C:\\Users\\james\\OneDrive\\Documents\\Vietnam_Project\\Dengue Paper\\V2 - PLOS review\\errors_colour_coded.xlsx")
df_rank = df.rank(axis=1)
df_rank.mean(axis=0)

df2 = pd.read_excel("C:\\Users\\james\\OneDrive\\Documents\\Vietnam_Project\\Dengue Paper\\V2 - PLOS review\\errors_colour_coded.xlsx", sheet_name="MAE")
df_rank2 = df2.rank(axis=1)
df_rank2.mean(axis=0)

# Generate subplot 1
g1 = sns.boxplot(data=df_rank, showmeans=True, meanprops={"marker":"o","markerfacecolor":"none", "markeredgecolor":"#36454F"}, ax=ax1)
ax1.set(xlabel='Model', ylabel='RMSE Rank')
# Rotate labels for better visibility
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, horizontalalignment='right')

# Generate subplot 2
g2 = sns.boxplot(data=df_rank2, showmeans=True, meanprops={"marker":"o","markerfacecolor":"none", "markeredgecolor":"#36454F"}, ax=ax2)
ax2.set(xlabel='Model', ylabel='MAE Rank')
# Rotate labels for better visibility
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, horizontalalignment='right')

# plt.savefig("C:\\Users\\james\\OneDrive\\Documents\\Vietnam_Project\\Figures\\df_model_rankings_light.tiff", dpi=600)
plt.show()


#########################################################################################################################
# Diarrhoea

# Read in data and calculate mean rankings
df = pd.read_excel("C:\\Users\\james\\OneDrive\\Documents\\Vietnam_Project\\FINAL_ERROR_RESULTS.xlsx", sheet_name="RMSE")
df_rank = df.rank(axis=1)
df_rank.mean(axis=0)

# Read in data and calculate mean rankings
df2 = pd.read_excel("C:\\Users\\james\\OneDrive\\Documents\\Vietnam_Project\\FINAL_ERROR_RESULTS.xlsx", sheet_name="MAE")
df_rank2 = df2.rank(axis=1)
df_rank2.mean(axis=0)

# Plot style
plt.rcParams['figure.figsize'] = [20.0, 7.0]
plt.rcParams['font.size'] = 16
matplotlib.rcParams.update({'font.size': 25})
sns.set_style('whitegrid')
sns.set_context("notebook", 1.4)

# Set up grid plots
fig = plt.figure()
AX = gridspec.GridSpec(2,6, bottom=0.2, wspace=0.5)
ax1  = plt.subplot(AX[:,0:3])
ax2 = plt.subplot(AX[:,3:6])

# Generate subplots
g1 = sns.boxplot(data=df_rank, showmeans=True, meanprops={"marker":"o","markerfacecolor":"none", "markeredgecolor":"#36454F"}, ax=ax1)
ax1.set(xlabel='Model', ylabel='RMSE Rank')
g2 = sns.boxplot(data=df_rank2, showmeans=True, meanprops={"marker":"o","markerfacecolor":"none", "markeredgecolor":"#36454F"}, ax=ax2)
ax2.set(xlabel='Model', ylabel='MAE Rank')

# plt.savefig("C:\\Users\\james\\OneDrive\\Documents\\Vietnam_Project\\Figures\\diarr_model_rankings_light.tiff", dpi=300)
plt.show()