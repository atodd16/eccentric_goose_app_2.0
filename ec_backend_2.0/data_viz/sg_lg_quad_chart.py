import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Read in long game short game data
quad_chart = pd.read_csv(r'C:\Users\aaron\PycharmProjects\eccentric_goose_model\eg_organized\quad_df.csv')

# Sort player names alphabetically
sorted_players = sorted(quad_chart['player_name'].unique())

# Initialize Dash app
app = Dash(__name__)

# Layout with dropdown for player filtering and toggle for display names
app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='player-dropdown',
            options=[{'label': player, 'value': player} for player in sorted_players],
            placeholder="Search or Select a Player",
            multi=True,  # Allows multiple players to be selected
            searchable=True,  # Enables the search bar functionality
            style={'width': '50%'}  # Adjust the width for better appearance
        ),
        html.Label("Toggle Display Names:"),
        dcc.Checklist(
            id='display-names-toggle',
            options=[{'label': 'Show Names', 'value': 'show'}],
            value=['show'],  # Default to showing names
            style={'margin-top': '10px'}
        )
    ], style={'display': 'flex', 'align-items': 'center', 'gap': '20px'}),
    dcc.Graph(id='quad-chart')
])

@app.callback(
    Output('quad-chart', 'figure'),
    Input('player-dropdown', 'value'),
    Input('display-names-toggle', 'value')
)
def update_chart(selected_players, display_toggle):
    # Handle case where no players are selected
    if selected_players is None or len(selected_players) == 0:
        filtered_df = quad_chart
    else:
        # Filter data based on selected players
        filtered_df = quad_chart[quad_chart['player_name'].isin(selected_players)]

    # Determine whether to display player names
    show_names = 'show' in display_toggle

    # Create the chart
    fig = px.scatter(
        filtered_df,
        x='12_mo_long_game',
        y='12_mo_short_game',
        text='player_name' if show_names else None,  # Conditionally display text
        hover_data={
            '12_mo_long_game': True,
            '12_mo_short_game': True,
            'player_name': True,
        },
        title='Player Performance: Long Game vs. Short Game'
    )

    # Add quadrant lines
    fig.update_layout(
        shapes=[
            # Vertical line at mean of 12_mo_long_game
            dict(type='line', x0=quad_chart['12_mo_long_game'].mean(),
                 x1=quad_chart['12_mo_long_game'].mean(),
                 y0=quad_chart['12_mo_short_game'].min(),
                 y1=quad_chart['12_mo_short_game'].max(), line=dict(dash='dot')),
            # Horizontal line at mean of 12_mo_short_game
            dict(type='line', x0=quad_chart['12_mo_long_game'].min(),
                 x1=quad_chart['12_mo_long_game'].max(),
                 y0=quad_chart['12_mo_short_game'].mean(),
                 y1=quad_chart['12_mo_short_game'].mean(), line=dict(dash='dot'))
        ]
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)


