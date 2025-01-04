# this script cleanses performance_data CSV and creates other necessary CSV files

import pandas as pd

# adjusts settings to print full dataframe
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

# read in performance_data CSV
performance_data = pd.read_csv(r'C:\Users\aaron\OneDrive\Documents\Golf Modeling\eccentric_goose_model_app\ec_backend_2.0\data_files\raw_data_files\performance_data.csv', index_col=0,
                               parse_dates=['event_completed'])

# read in event_data_cleansed CSV
event_data = pd.read_csv(r'C:\Users\aaron\OneDrive\Documents\Golf Modeling\eccentric_goose_model_app\ec_backend_2.0\data_files\cleansed_data_files\event_data_cleansed', index_col=0,
                         parse_dates=['event_completed'])

# drops columns where event_id is blank
performance_data = performance_data.dropna(subset=['event_completed'])

# merge distinct_event_id into performance_data
performance_data = performance_data.merge(event_data[['event_id', 'event_completed', 'distinct_event_id']], on=['event_id', 'event_completed'], how='left')

# adds a 'year' column based off 'event_completed'
performance_data['year'] = pd.to_datetime(performance_data['event_completed']).dt.year.astype(int)


print(performance_data)





