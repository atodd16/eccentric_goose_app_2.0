# this script cleanses performance_data CSV and creates other necessary CSV files

import pandas as pd

# adjusts settings to print full dataframe
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

# read in performance_data CSV
performance_data = pd.read_csv(r'C:\Users\aaron\OneDrive\Documents\Golf Modeling\eccentric_goose_model_app\ec_backend_2.0\data_files\raw_data_files\performance_data.csv', index_col=0,
                               parse_dates=['event_completed'])

# read in event_data_cleansed CSV
event_data = pd.read_csv(r'C:\Users\aaron\OneDrive\Documents\Golf Modeling\eccentric_goose_model_app\ec_backend_2.0\data_files\cleansed_data_files\event_data_cleansed.csv', index_col=0,
                         parse_dates=['event_completed'])

# read in aggregated_datagolf_rankings CSV
aggregated_data_golf_rankings = pd.read_csv(
    r'C:\Users\aaron\OneDrive\Documents\Golf Modeling\eccentric_goose_model_app\ec_backend_2.0\data_files\cleansed_data_files\aggregated_datagolf_rankings.csv',
    index_col=0,
    parse_dates=['dg_ranking_start', 'dg_ranking_end']
)

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

# creates new dataframe 'dg_ranked_performance_data' which merges 'dg_rank' from 'aggregated_datagolf_ranking' into performance data and filters out null values
merged_df = pd.merge(performance_data, aggregated_data_golf_rankings[['dg_id', 'dg_rank','dg_ranking_start', 'dg_ranking_end']], on='dg_id', how='left')

dg_ranked_performance_data = merged_df[((merged_df['event_completed'] >= merged_df['dg_ranking_start']) &
                         (merged_df['event_completed'] <= merged_df['dg_ranking_end']))]

performance_data_clean = dg_ranked_performance_data.copy()

# creates new dataframe 'event_round_dg_rank' which evaluates the average dg_rank by event and round
event_round_dg_rank = (
    dg_ranked_performance_data
    .groupby(['distinct_event_id', 'round_completed', 'round'])
    .agg(
        avg_dg_rank=('dg_rank', 'mean'),
        total_count=('dg_rank', 'count')
    )
    .reset_index()
)

# add 12-month rolling sg statistics columns to 'dg_ranked_performance' dataframe

# NEED TO ADD THE OTHER 12 MONTH ROLLING AVERAGE COLUMNS - ADDITIONALLY SEE IF YOU CAN FILTER WITHIN THE FUNCTIONS TO SWITCH BETWEEN ADVANCED SG STATS 'Y' & 'N'

performance_data_clean = performance_data_clean[performance_data_clean['advanced_sg_stats'] == 'Y']


performance_data_clean.reset_index(drop=True, inplace=True)

performance_data_clean['sg_ott_rolling_avg'] = (
    performance_data_clean
    .groupby('dg_id', group_keys=False)
    .apply(
        lambda group: group.rolling('365D', on='round_completed', min_periods=1)['sg_ott'].mean(), include_groups=False
    )
    .reset_index(level=0, drop=True)
 )


print(performance_data_clean)



# performance_data_clean['sg_app_rolling_avg'] = performance_data_clean.groupby('dg_id', group_keys=False).apply(
#     lambda group: group.sort_values('round_completed').rolling('365D', on='round_completed', min_periods=1)['sg_app'].mean(), include_groups=False
# ).reset_index(level=0, drop=True)

# performance_data_clean['sg_arg_rolling_avg'] = performance_data_clean.groupby('dg_id', group_keys=False).apply(
#     lambda group: group.sort_values('round_completed').rolling('365D', on='round_completed', min_periods=1)['sg_arg'].mean(), include_groups=False
# ).reset_index(level=0, drop=True)

# performance_data_clean['sg_putt_rolling_avg'] = performance_data_clean.groupby('dg_id', group_keys=False).apply(
#     lambda group: group.sort_values('round_completed').rolling('365D', on='round_completed', min_periods=1)['sg_putt'].mean(), include_groups=False
# ).reset_index(level=0, drop=True)

# performance_data_clean['sg_total_rolling_avg'] = performance_data_clean.groupby('dg_id',group_keys=False).apply(
#     lambda group: group.sort_values('round_completed').rolling('365D', on='round_completed', min_periods=1)['sg_total'].mean(), include_groups=False
# ).reset_index(level=0, drop=True)

performance_data_clean.to_csv(r'C:\Users\aaron\OneDrive\Documents\Golf Modeling\eccentric_goose_model_app\ec_backend_2.0\data_files\scratch\performance_data_clean.csv')












