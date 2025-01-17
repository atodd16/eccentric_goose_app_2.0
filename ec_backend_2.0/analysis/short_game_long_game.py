import pandas as pd

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

short_game_long_game_quad = performance_data.groupby('dg_id', group_keys=False).apply(
    lambda group: pd.DataFrame({
        'player_name': group['player_name'],
        'short_game_rolling_mean': group.rolling('365D', on='round_completed', min_periods=1)['sg_short_game'].mean(),
        'long_game_rolling_mean': group.rolling('365D', on='round_completed', min_periods=1)['sg_long_game'].mean(),
    }), include_groups=False
).reset_index(drop=True)

test = performance_data.groupby('dg_id', group_keys=False)
print(test)

#short_game_long_game_quad.reset_index(drop=True, inplace=True)



