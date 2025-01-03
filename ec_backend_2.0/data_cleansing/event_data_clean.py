# this script cleanses event_data CSV and creates other necessary CSV files

import pandas as pd

# adjusts settings to print full dataframe
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

# read in performance_data CSV
event_data = pd.read_csv(r'C:\Users\aaron\OneDrive\Documents\Golf Modeling\eccentric_goose_model_app\ec_backend_2.0\data_files\raw_data_files\event_data.csv')

# creates new column 'distinct_event_id' which differentiates from tour to tour
event_data['distinct_event_id'] = pd.factorize(event_data[['event_id', 'tour']].apply(tuple, axis=1)) [0] + 1

# saves CSV to 'cleansed_data_files'
event_data.to_csv(r'C:\Users\aaron\OneDrive\Documents\Golf Modeling\eccentric_goose_model_app\ec_backend_2.0\data_files\cleansed_data_files\event_data_cleansed')


