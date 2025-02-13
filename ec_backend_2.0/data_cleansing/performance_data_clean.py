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

# merge tour and distinct_event_id into performance_data
performance_data = performance_data.merge(event_data[['event_id', 'event_completed', 'tour', 'distinct_event_id']], on=['event_id', 'event_completed'], how='left')

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
performance_data['advanced_sg_stats'] = performance_data[['sg_ott', 'sg_app', 'sg_arg', 'sg_putt']].notna().all(axis=1).map({True: 'Y', False: 'N'})

# create 12 month rolling count for advanced strokes gained rounds
adv_sg = performance_data[performance_data['advanced_sg_stats'] == 'Y'].copy()

# Convert 'round_completed' to datetime using pd.to_datetime
adv_sg['round_completed'] = pd.to_datetime(adv_sg['round_completed'])

# Sort the DataFrame by 'round_completed' to ensure proper rolling calculation
adv_sg = adv_sg.sort_values('round_completed')

# Group by 'dg_id' and compute the rolling 365-day count of 'player_name'
adv_sg = (
    adv_sg.groupby('dg_id')
    .apply(lambda group: group.set_index('round_completed')['player_name']
           .rolling('365D').count(), include_groups=False)
    .reset_index(name='#_of_sga_rounds')
)

# merges '#_of_sga_rounds' into 'performance_data'
performance_data = performance_data.merge(
    adv_sg[['round_completed', 'dg_id', '#_of_sga_rounds']],
    on=['round_completed', 'dg_id'],
    how='left'
)

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

dg_ranked_performance_data = dg_ranked_performance_data.copy()

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

# merge round level dg rank into 'dg_ranked_performance' and round 'dg_rank'
dg_ranked_performance_data = pd.merge(dg_ranked_performance_data, event_round_dg_rank[['distinct_event_id', 'round_completed', 'round', 'avg_dg_rank']], on=['distinct_event_id', 'round_completed', 'round'], how='left')
dg_ranked_performance_data['avg_dg_rank'] = dg_ranked_performance_data['avg_dg_rank'].round()

# saves as 'performance_data_cleansed' under cleansed data files
dg_ranked_performance_data.to_csv(r'C:\Users\aaron\OneDrive\Documents\Golf Modeling\eccentric_goose_model_app\ec_backend_2.0\data_files\cleansed_data_files\performance_data_cleansed.csv')

# add 12-month rolling sg statistics columns to 'dg_ranked_performance' dataframe
# resets index
dg_ranked_performance_data.reset_index(drop=True, inplace=True)

# adds 12 month rolling avg for 'sg_ott'
dg_ranked_performance_data['sg_ott_rolling_avg'] = (
    dg_ranked_performance_data
    .groupby('dg_id', group_keys=False)
    .apply(
        lambda group: group.rolling('365D', on='round_completed', min_periods=1)['sg_ott'].mean(), include_groups=False
    )
    .reset_index(level=0, drop=True)
 )

# adds 12 month rolling avg for 'sg_app'
dg_ranked_performance_data['sg_app_rolling_avg'] = (
    dg_ranked_performance_data
    .groupby('dg_id', group_keys=False)
    .apply(
        lambda group: group.rolling('365D', on='round_completed', min_periods=1)['sg_app'].mean(), include_groups=False
    )
    .reset_index(level=0, drop=True)
 )

# adds 12 month rolling avg for 'sg_arg'
dg_ranked_performance_data['sg_arg_rolling_avg'] = (
    dg_ranked_performance_data
    .groupby('dg_id', group_keys=False)
    .apply(
        lambda group: group.rolling('365D', on='round_completed', min_periods=1)['sg_arg'].mean(), include_groups=False
    )
    .reset_index(level=0, drop=True)
 )

# adds 12 month rolling avg for 'sg_putt'
dg_ranked_performance_data['sg_putt_rolling_avg'] = (
    dg_ranked_performance_data
    .groupby('dg_id', group_keys=False)
    .apply(
        lambda group: group.rolling('365D', on='round_completed', min_periods=1)['sg_putt'].mean(), include_groups=False
    )
    .reset_index(level=0, drop=True)
 )

# adds 12 month rolling avg for 'sg_total'
dg_ranked_performance_data['sg_total_rolling_avg'] = (
    dg_ranked_performance_data
    .groupby('dg_id', group_keys=False)
    .apply(
        lambda group: group.rolling('365D', on='round_completed', min_periods=1)['sg_total'].mean(), include_groups=False
    )
    .reset_index(level=0, drop=True)
 )

# add rows which calculate the delta between actual score and sg rolling averages
dg_ranked_performance_data['sg_ott_delta'] = dg_ranked_performance_data['sg_ott'] - dg_ranked_performance_data['sg_ott_rolling_avg']
dg_ranked_performance_data['sg_app_delta'] = dg_ranked_performance_data['sg_app'] - dg_ranked_performance_data['sg_app_rolling_avg']
dg_ranked_performance_data['sg_arg_delta'] = dg_ranked_performance_data['sg_arg'] - dg_ranked_performance_data['sg_arg_rolling_avg']
dg_ranked_performance_data['sg_putt_delta'] = dg_ranked_performance_data['sg_putt'] - dg_ranked_performance_data['sg_putt_rolling_avg']
dg_ranked_performance_data['sg_total_delta'] = dg_ranked_performance_data['sg_total'] - dg_ranked_performance_data['sg_total_rolling_avg']


# drops all players who have completed >1st Q in rounds
q1 = dg_ranked_performance_data['#_of_rounds'].quantile(.25)
q2 = dg_ranked_performance_data['#_of_rounds'].quantile(.50)
q3 = dg_ranked_performance_data['#_of_rounds'].quantile(.75)
print(f'Q1: {q1}, Q2:{q2}, Q3:{q3}')

dg_ranked_performance_data = dg_ranked_performance_data[dg_ranked_performance_data['#_of_rounds'] > q1]

# filters out non-pga tour rounds
dg_ranked_performance_data_pga = dg_ranked_performance_data[dg_ranked_performance_data['tour'] == 'pga']

# creates dataframe summarizing average sg_delta by dg_rank
dg_rank_performance_matrix = dg_ranked_performance_data_pga.groupby(['avg_dg_rank']).agg(
    sg_ott_avg_perf_delta=('sg_ott_delta', 'mean'),
    sg_app_avg_perf_delta=('sg_app_delta', 'mean'),
    sg_arg_avg_perf_delta=('sg_arg_delta', 'mean'),
    sg_putt_avg_perf_delta=('sg_putt_delta', 'mean'),
    sg_total_avg_perf_delta=('sg_total_delta', 'mean'),
    count=('sg_total_delta', 'count'),
).reset_index()

# removes 'avg_dg_rank' values from 'dg_rank_performance_matrix' under .10 percentile
p10 = dg_rank_performance_matrix['count'].quantile(.1)
p25 = dg_rank_performance_matrix['count'].quantile(.25)
p50 = dg_rank_performance_matrix['count'].quantile(.50)
p75 = dg_rank_performance_matrix['count'].quantile(.75)
print(f'p10:{p10},p25:{p25}, p50:{p50}, p75: {p75}')

dg_rank_performance_matrix = dg_rank_performance_matrix[dg_rank_performance_matrix['count'] > p10]

dg_rank_performance_matrix.reset_index(drop=True, inplace=True)

# saves as 'dg_rank_performance_matrix' in cleansed data files
dg_rank_performance_matrix.to_csv(r'C:\Users\aaron\OneDrive\Documents\Golf Modeling\eccentric_goose_model_app\ec_backend_2.0\data_files\cleansed_data_files\dg_rank_performance_matrix.csv')

print(dg_rank_performance_matrix)















