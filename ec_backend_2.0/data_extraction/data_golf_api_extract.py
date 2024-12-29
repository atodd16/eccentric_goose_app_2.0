# this script uses the data_files golf api to extract 3 primary data_files sources 1.) player+data_files 2.) event_data 3.) performance_data

import requests
import pandas as pd

# adjusts settings to print full dataframe
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

# 1.) api request for player_data

# define base api url
url = 'https://feeds.datagolf.com/get-player-list'

# defines api parameters
params = {
    'file_format': 'json',
    'key': '78d94f28ac5a1b6fbe373b25fbe1'
}

# make GET request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    player_data = response.json()

print('player data connection successful')

# convert to dataframe
player_data = pd.DataFrame(player_data)

# saves data frame to CSV
player_data.to_csv(r'C:\Users\aaron\OneDrive\Documents\Golf Modeling\eccentric_goose_model_app\ec_backend_2.0\data_files\raw_data_files\player_data.csv')

print('player data successfully saved')


# 2.) api request for event_data

# define the base url
url = 'https://feeds.datagolf.com/historical-raw-data/event-list'

# define the api parameters
params = {
    'file_format': 'json',
    'key': '78d94f28ac5a1b6fbe373b25fbe1'
}

# make GET request
response = requests.get(url, params=params)

# check if the request was successful
if response.status_code == 200:
    event_data = response.json()
print('event data connection successful')

# convert to dataframe
event_data = pd.DataFrame(event_data)

# saves data frame to CSV
event_data.to_csv(r'C:\Users\aaron\OneDrive\Documents\Golf Modeling\eccentric_goose_model_app\ec_backend_2.0\data_files\raw_data_files\event_data.csv')

print('event data successfully saved')

# creates new column with distinct event id
event_data['distinct_event_id'] = pd.factorize(event_data[['event_id', 'tour']].apply(tuple, axis=1)) [0] + 1

# filter event data and save as csv
performance_data_api_params = event_data[(event_data['tour'].isin(['pga', 'liv', 'euro'])) &
                 (event_data['calendar_year'].between(2020, 2024))]

# saves data frame to CSV
performance_data_api_params.to_csv(r'C:\Users\aaron\OneDrive\Documents\Golf Modeling\eccentric_goose_model_app\ec_backend_2.0\data_files\raw_data_files\performance_data_api_params.csv')
print('performance data api params successfully saved')

# 3.) api request performance_data

# initialize a list to store the flattened data across all events
all_flattened_data = []

# iterate over the DataFrame rows
for index, row in performance_data_api_params.iterrows():
    calendar_year = row['calendar_year']
    event_id = row['event_id']
    tour = row['tour']

    # Define the base URL for the API
    url = 'https://feeds.datagolf.com/historical-raw-data/rounds'

    # define the parameters for each event
    params = {
        'tour': tour,
        'event_id': event_id,
        'year': calendar_year,
        'file_format': 'json',
        'key': '78d94f28ac5a1b6fbe373b25fbe1'  # Replace with your actual API key
    }

    # make the GET request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        print('performance data connection successful')

        # Initialize an empty list to store flattened data for this event
        flattened_data = []

        if 'scores' in data:
            for player in data['scores']:
                for round_key in ['round_1', 'round_2', 'round_3', 'round_4']:
                    if round_key in player:
                        round_data = player[round_key]
                        round_data['dg_id'] = player['dg_id']
                        round_data['fin_text'] = player['fin_text']
                        round_data['player_name'] = player['player_name']
                        round_data['round'] = round_key
                        round_data['event_completed'] = data['event_completed']
                        round_data['event_id'] = data['event_id']
                        round_data['event_name'] = data['event_name']

                        # Check if this combination of dg_id and round_key already exists in flattened_data
                        unique_key = (round_data['dg_id'], round_data['round'])
                        if not any((d['dg_id'], d['round']) == unique_key for d in flattened_data):
                            flattened_data.append(round_data)

            # Append this event's flattened data to the overall list
            all_flattened_data.extend(flattened_data)

        else:
            print(f"No 'scores' data found for event {event_id}.")
    else:
        print(f"Request for event {event_id} failed with status code {response.status_code}")

# Convert the accumulated flattened data to a DataFrame
performance_data = pd.DataFrame(all_flattened_data)

# save dataframe to CSV
performance_data.to_csv(r'C:\Users\aaron\OneDrive\Documents\Golf Modeling\eccentric_goose_model_app\ec_backend_2.0\data_files\raw_data_files\performance_data.csv')
print('performance data successfully saved')
