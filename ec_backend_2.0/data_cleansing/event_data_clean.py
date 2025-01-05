# this script cleanses event_data CSV and creates other necessary CSV files

import pandas as pd

# adjusts settings to print full dataframe
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

# read in performance_data CSV
event_data = pd.read_csv(r'C:\Users\aaron\OneDrive\Documents\Golf Modeling\eccentric_goose_model_app\ec_backend_2.0\data_files\raw_data_files\event_data.csv', index_col=0)

# creates new column 'distinct_event_id' which differentiates event_id from tour to tour
event_data['distinct_event_id'] = pd.factorize(event_data[['event_id', 'tour']].apply(tuple, axis=1)) [0] + 1

# rename 'date' to 'event_completed'
event_data.rename(columns={'date':'event_completed'}, inplace=True)

# saves CSV to 'cleansed_data_files'
event_data.to_csv(r'C:\Users\aaron\OneDrive\Documents\Golf Modeling\eccentric_goose_model_app\ec_backend_2.0\data_files\cleansed_data_files\event_data_cleansed.csv')

#event_data = event_data[event_data['event_name'] == 'Alfred Dunhill Championship #2']

print(event_data)

