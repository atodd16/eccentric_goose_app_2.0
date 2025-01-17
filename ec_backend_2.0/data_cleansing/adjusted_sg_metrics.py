import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# adjusts settings to print full dataframe
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

# import csv files
dg_rank_performance_matrix = pd.read_csv(r'C:\Users\aaron\OneDrive\Documents\Golf Modeling\eccentric_goose_model_app\ec_backend_2.0\data_files\cleansed_data_files\dg_rank_performance_matrix.csv', index_col=0)
performance_data = pd.read_csv(r'C:\Users\aaron\OneDrive\Documents\Golf Modeling\eccentric_goose_model_app\ec_backend_2.0\data_files\cleansed_data_files\performance_data_cleansed.csv', index_col=0)

# establish target dg rank
target_pga_dg_rank = (dg_rank_performance_matrix['avg_dg_rank'] * dg_rank_performance_matrix['count']).sum() / dg_rank_performance_matrix['count'].sum()
print(target_pga_dg_rank)

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

# calculate sg total statistics at target rank
target_sg_total = model.intercept_ + (model.coef_ * target_pga_dg_rank)
print(f'target sg total: {target_sg_total}')


# adjust sg total statistics to target ranking
performance_data['adj_sg_total'] = performance_data.apply(
    lambda row: row['sg_total'] + (target_sg_total - (model.intercept_ + model.coef_ * row['avg_dg_rank'])),
    axis=1
)

# sg_ott strength of field sg regression analysis
# filter out blanks
dg_rank_performance_matrix_no_nan = dg_rank_performance_matrix[dg_rank_performance_matrix['sg_ott_avg_perf_delta'].notna()]

# assign variables
X = dg_rank_performance_matrix_no_nan[['avg_dg_rank']]  # Features should be a DataFrame
y = dg_rank_performance_matrix_no_nan['sg_ott_avg_perf_delta']  # Target should be a Series

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


print(f"SG OTT: Mean Squared Error: {mse}")
print(f"SG OTT: R² Score: {r2}")

# view model coefficients and intercept
print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

# calculate sg total statistics at target rank
target_sg_ott = model.intercept_ + (model.coef_ * target_pga_dg_rank)
print(f'target sg ott: {target_sg_ott}')


# adjust sg total statistics to target ranking
performance_data['adj_sg_ott'] = performance_data.apply(
    lambda row: row['sg_ott'] + (target_sg_total - (model.intercept_ + model.coef_ * row['avg_dg_rank'])),
    axis=1
)

# sg_app strength of field sg regression analysis
# filter out blanks
dg_rank_performance_matrix_no_nan = dg_rank_performance_matrix[dg_rank_performance_matrix['sg_app_avg_perf_delta'].notna()]

# assign variables
X = dg_rank_performance_matrix_no_nan[['avg_dg_rank']]  # Features should be a DataFrame
y = dg_rank_performance_matrix_no_nan['sg_app_avg_perf_delta']  # Target should be a Series

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


print(f"SG APP: Mean Squared Error: {mse}")
print(f"SG APP: R² Score: {r2}")

# view model coefficients and intercept
print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

# calculate sg total statistics at target rank
target_sg_app = model.intercept_ + (model.coef_ * target_pga_dg_rank)
print(f'target sg app: {target_sg_app}')


# adjust sg total statistics to target ranking
performance_data['adj_sg_app'] = performance_data.apply(
    lambda row: row['sg_app'] + (target_sg_total - (model.intercept_ + model.coef_ * row['avg_dg_rank'])),
    axis=1
)

# sg_arg strength of field sg regression analysis
# filter out blanks
dg_rank_performance_matrix_no_nan = dg_rank_performance_matrix[dg_rank_performance_matrix['sg_arg_avg_perf_delta'].notna()]

# assign variables
X = dg_rank_performance_matrix_no_nan[['avg_dg_rank']]  # Features should be a DataFrame
y = dg_rank_performance_matrix_no_nan['sg_arg_avg_perf_delta']  # Target should be a Series

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


print(f"SG ARG: Mean Squared Error: {mse}")
print(f"SG ARG: R² Score: {r2}")

# view model coefficients and intercept
print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

# calculate sg total statistics at target rank
target_sg_arg = model.intercept_ + (model.coef_ * target_pga_dg_rank)
print(f'target sg arg: {target_sg_arg}')


# adjust sg total statistics to target ranking
performance_data['adj_sg_arg'] = performance_data.apply(
    lambda row: row['sg_arg'] + (target_sg_total - (model.intercept_ + model.coef_ * row['avg_dg_rank'])),
    axis=1
)

# sg_putt strength of field sg regression analysis
# filter out blanks
dg_rank_performance_matrix_no_nan = dg_rank_performance_matrix[dg_rank_performance_matrix['sg_putt_avg_perf_delta'].notna()]

# assign variables
X = dg_rank_performance_matrix_no_nan[['avg_dg_rank']]  # Features should be a DataFrame
y = dg_rank_performance_matrix_no_nan['sg_putt_avg_perf_delta']  # Target should be a Series

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


print(f"SG PUTT: Mean Squared Error: {mse}")
print(f"SG PUTT: R² Score: {r2}")

# view model coefficients and intercept
print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

# calculate sg total statistics at target rank
target_sg_putt = model.intercept_ + (model.coef_ * target_pga_dg_rank)
print(f'target sg putt: {target_sg_putt}')


# adjust sg total statistics to target ranking
performance_data['adj_sg_putt'] = performance_data.apply(
    lambda row: row['sg_putt'] + (target_sg_total - (model.intercept_ + model.coef_ * row['avg_dg_rank'])),
    axis=1
)



