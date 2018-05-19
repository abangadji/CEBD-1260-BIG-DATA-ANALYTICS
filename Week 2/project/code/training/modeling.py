import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.externals import joblib

df = pd.read_csv('../../data/processed/house_pricing.csv')

# Create linear regression object
model = linear_model.LinearRegression()

columns = ['bedrooms', 'bathrooms', 'sqft_living15', 'grade', 'condition']

# Train the model using the training sets
model.fit(df[columns], df['price'])

# Print the Coefficients
print 'Coefficients', np.round(model.coef_,1)
print 'Interception', round(model.intercept_,1)
print ''
for i, col in enumerate(columns):
    print col, round(model.coef_[i],1)

joblib.dump(model, '../../model/linear_regression.pkl')
