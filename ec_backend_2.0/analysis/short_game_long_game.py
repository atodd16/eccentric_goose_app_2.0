import pandas as pd
from datetime import datetime

# adjusts settings to print full dataframe
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

performance_data = pd.read_csv(r'C:\Users\aaron\OneDrive\Documents\Golf Modeling\eccentric_goose_model_app\ec_backend_2.0\data_files\cleansed_data_files\perf_data_adj_sg.csv',
                             index_col=0)

# add 'short_game' and 'long_game' calcs
performance_data['sg_long_game'] = performance_data['adj_sg_ott'] + performance_data['adj_sg_app']
performance_data['sg_short_game'] = performance_data['adj_sg_arg'] + performance_data['adj_sg_putt']

# drop values without advanced sg statistics
performance_data = performance_data[performance_data['advanced_sg_stats'] == 'Y'].reset_index()

# set 'round_completed as datetime
performance_data['round_completed'] = pd.to_datetime(performance_data['round_completed'], errors='coerce')

# sort by dg_id and date
performance_data = performance_data.sort_values(by=['dg_id', 'round_completed'])

# calculate 12 mo long-game rolling average
performance_data['12_mo_long_game']= (
    performance_data.groupby('dg_id')
    .rolling('365D', on='round_completed')['sg_long_game']
    .mean()
    .reset_index(drop=True)
)

# calculate 12 mo short-game rolling average
performance_data['12_mo_short_game']= (
    performance_data.groupby('dg_id')
    .rolling('365D', on='round_completed')['sg_short_game']
    .mean()
    .reset_index(drop=True)
)

today = pd.Timestamp(datetime.now().date())

# filter data for each player to get the closest record to today's date
latest_rnd_df = (
    performance_data[performance_data['round_completed'] <= today]
    .sort_values(['dg_id', 'round_completed'], ascending=[True, False])
    .groupby('dg_id', as_index=False)
    .first()
)

p0 = latest_rnd_df['#_of_sga_rounds'].quantile(0.0)
p25 = latest_rnd_df['#_of_sga_rounds'].quantile(0.25)
p50 = latest_rnd_df['#_of_sga_rounds'].quantile(0.5)
p75 = latest_rnd_df['#_of_sga_rounds'].quantile(0.75)
p100 = latest_rnd_df['#_of_sga_rounds'].quantile(0.1)

print(p0)
print(p25)
print(p50)
print(p75)
print(p100)

latest_rnd_df = latest_rnd_df[latest_rnd_df['#_of_sga_rounds'] > p50]

# create quad chart dg
quad_df = latest_rnd_df[['dg_id', 'player_name', '12_mo_long_game','12_mo_short_game', '#_of_rounds', 'tour']]

quad_df.to_csv(r'C:\Users\aaron\OneDrive\Documents\Golf Modeling\eccentric_goose_model_app\ec_backend_2.0\data_files\chart_data_files\quad_df.csv')

print(quad_df)


