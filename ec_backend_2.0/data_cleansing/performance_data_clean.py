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

# create 'round_completed' column based on round and 'event_completed' values and convert to datetime
performance_data['round_completed'] = performance_data.apply(
    lambda row: row['event_completed'] - pd.Timedelta(days=3) if row['round'] == 'round_1' else
                row['event_completed'] - pd.Timedelta(days=2) if row['round'] == 'round_2' else
                row['event_completed'] - pd.Timedelta(days=1) if row['round'] == 'round_3' else
                row['event_completed'] if row['round'] == 'round_4' else None,
    axis=1)

performance_data['round_completed']=pd.to_datetime(performance_data['round_completed'], errors='coerce')

# create new column 'advanced_sg_stats' based on whether specific sg columns have non-null values
performance_data['advanced_sg_stats']=performance_data[['sg_ott', 'sg_app', 'sg_arg', 'sg_putt']].notna().all(axis=1).map({True:'Y', False:'N'})

# count the number of rounds each player has had in the last 12 months

# sorts 'performance_data' by 'dg_id' and 'round_completed'
performance_data = performance_data.sort_values(by=['dg_id', 'round_completed'])

# creates dataframe 'rolling_counts' which groups by 'dg_id' and counts number of round over last 12 months
rolling_counts = (
    performance_data.groupby('dg_id')
    .apply(lambda group: group.set_index('round_completed')['player_name']
           .rolling('365D').count(), include_groups=False)
    .reset_index()
)

# renames 'player_name' to '#_of_rounds'
rolling_counts.rename(columns={'player_name' : '#_of_rounds'}, inplace=True)

# merges '#_of_rounds' into 'performance_data'
performance_data = performance_data.merge(
    rolling_counts[['round_completed', 'dg_id', '#_of_rounds']],
    on=['round_completed', 'dg_id']
)












