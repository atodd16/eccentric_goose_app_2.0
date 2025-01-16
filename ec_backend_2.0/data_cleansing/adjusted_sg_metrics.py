import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

dg_rank_performance_matrix = pd.read_csv(r'C:\Users\aaron\OneDrive\Documents\Golf Modeling\eccentric_goose_model_app\ec_backend_2.0\data_files\cleansed_data_files\dg_rank_performance_matrix.csv')

# sg_total strength of field sg regression analysis
# assign variables
X = dg_rank_performance_matrix[['avg_dg_rank']]  # Features should be a DataFrame
y = dg_rank_performance_matrix['sg_total_avg_perf_delta']  # Target should be a Series

# split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# create linear model
model = LinearRegression()

# train model on training data
model.fit(X_train, y_train)

# make predictions on the test set
y_pred = model.predict(X_test)

# evaluate the model and create functions
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)


print(f"SG Total: Mean Squared Error: {mse}")
print(f"SG Total: R² Score: {r2}")

# view model coefficients and intercept
print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

# plot the data points
plt.scatter(X_test, y_test, color='blue', label='med_sg_deltas')

# plot the regression line
plt.plot(X_test, y_pred, color='red', linewidth=2, label = 'regression line')

# add labels
plt.xlabel('avg dg rank')
plt.ylabel('sg total performance delta')
plt.title('avg dg rank vs median sg total delta')
plt.legend()

plt.show()
