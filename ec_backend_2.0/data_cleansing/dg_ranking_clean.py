import pandas as pd
import os
from datetime import datetime, timedelta

# Specify the folder path
folder_path = r'C:\Users\aaron\OneDrive\Documents\Golf Modeling\eccentric_goose_model_app\ec_backend_2.0\data_files\raw_data_files\data_golf_ranking_files'


# Create an empty DataFrame to hold all the data
aggregated_datagolf_rankings = pd.DataFrame()

# Iterate through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)

        # Read the CSV file into a dataframe
        df = pd.read_csv(file_path)

        # Get date values and convert format
        title = os.path.splitext(filename)[0]  # Changed to use filename instead of file_path
        last_8_digits = title[-8:]
        date_obj = datetime.strptime(last_8_digits, '%Y%m%d')
        formatted_start_date = date_obj.strftime('%m/%d/%Y')
        end_date_obj = date_obj + timedelta(days=6)
        formatted_end_date = end_date_obj.strftime('%m/%d/%Y')

        # Add values to the dataframe
        df['dg_ranking_start'] = formatted_start_date
        df['dg_ranking_end'] = formatted_end_date

        # Save the updated DataFrame back to the CSV file (optional)
        df.to_csv(file_path, index=False)

        # Append the current dataframe to the aggregated dataframe
        aggregated_datagolf_rankings = pd.concat([aggregated_datagolf_rankings, df], ignore_index=True)

# Add dg_id
player_information = pd.read_csv(r'C:\Users\aaron\OneDrive\Documents\Golf Modeling\eccentric_goose_model_app\ec_backend_2.0\data_files\raw_data_files\player_data.csv')
lookup_column = player_information[['player_name', 'dg_id']]
aggregated_datagolf_rankings = aggregated_datagolf_rankings.merge(lookup_column, on='player_name', how='left')

# Save the aggregated dataframe to a new CSV file
aggregated_datagolf_rankings.to_csv(r'C:\Users\aaron\OneDrive\Documents\Golf Modeling\eccentric_goose_model_app\ec_backend_2.0\data_files\cleansed_data_files\aggregated_datagolf_rankings.csv', index=False)

print('Process completed.')