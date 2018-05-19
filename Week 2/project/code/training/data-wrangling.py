import pandas as pd
import numpy as np

df_listing = pd.read_csv('../../data/raw/kc_house_data.csv')
df_walking_score = pd.read_csv('../../data/raw/walking_score.csv')
df_income = pd.read_csv('../../data/raw/ZIP-3.csv')

print('')
print('Total # houses', len(df_listing))

# Summarizing your data for inspection
print('Listings')
print(df_listing.head())
print(df_listing.describe())
print('')
print('Walking Score')
print(df_walking_score.head())
print(df_walking_score.describe())
print('')
print('Income')
print(df_income.head())
print(df_income.describe())

# Fixing column name
df_income.columns = ['zipcode', 'median_income', 'mean_income', 'population']

# Converting data types
df_listing['date'] = pd.to_datetime(df_listing['date'])
df_income['median_income'] = df_income['median_income'].str.replace(',', '').astype(float)
df_income['mean_income'] = df_income['mean_income'].str.replace(',', '').astype(float)
df_income['population'] = pd.to_numeric(df_income['population'].str.replace(',', ''))

# Dealing with missing values
print('')
print('Missing Values')
print(df_listing.isnull().sum())
print(df_walking_score.isnull().sum())
print(df_income.isnull().sum())

df_walking_score = df_walking_score.fillna(-1)
df_income['mean_income'] = df_income['mean_income'].fillna(df_income['median_income'])

# Dealing with outliers
houses_to_remove = []

# remove based on bedrooms
m = np.mean(df_listing['bedrooms'])
s = np.std(df_listing['bedrooms'])
print('')
print('Statistics about #bedrooms', m, s)
houses_to_remove = houses_to_remove + list(df_listing[df_listing['bedrooms']>m+3.0*s].index)

# remove based on zipcode and price
for zipcode in df_listing['zipcode'].unique():
    df_zipcode = df_listing[df_listing['zipcode']==zipcode]
    m = np.mean(df_zipcode['price'])
    s = np.std(df_zipcode['price'])
    houses_to_remove = houses_to_remove + list(df_zipcode[df_zipcode['price']>m+3.0*s].index)
print('')
print('# houses to remove', len(houses_to_remove))

df_listing = df_listing[~df_listing.index.isin(houses_to_remove)]

# Merging Data Sets
df_merge = df_listing.copy()
df_merge = df_merge.merge(df_walking_score, on='zipcode', how='left')
df_merge = df_merge.merge(df_income, on='zipcode', how='left')

print('')
print('Total # houses', len(df_merge))

# Saving the processed file
df_merge.to_csv('../../data/processed/house_pricing.csv', index=False)