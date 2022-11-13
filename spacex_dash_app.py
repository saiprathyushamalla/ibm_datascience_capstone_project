# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("C:/Users/vsama/Downloads/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    ],
                                    value='ALL',
                                    placeholder="Select a Launch Site",
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                # Function decorator to specify function input and output
                                # figure={}
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0',
                                        1000: '1000',
                                        2000:'2000',
                                        3000:'3000',
                                        4000: '4000',
                                        5000 : '5000',
                                        6000: '6000',
                                        7000 : '7000',
                                        8000: '8000',
                                        9000 : '9000',
                                        10000: '10000'},
                                    value=[0, 10000]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))
def success_pie_chart(entered_site):
    filtered_df = spacex_df[['Launch Site', 'class']]
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches by Site')
        # print('All sites are considered')
        return fig
    else:
        # return the outcomes piechart for a selected site
        # fig = px.pie(filtered_df[filtered_df['Launch Site'] == entered_site], values='class', 
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        filtered_df = filtered_df.groupby(['class'])['class'].count().reset_index(name='count')
        fig = px.pie(filtered_df, values='count', 
        names='class', 
        title=f'Total Success Launches for site {entered_site}')
        # print(f'Only one site {entered_site} is considered')
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
    Input(component_id='payload-slider', component_property='value')])

def success_payload_scatter_chart(entered_site, payload_mass):
    filtered_df = spacex_df[(payload_mass[0] < spacex_df['Payload Mass (kg)']) & (spacex_df['Payload Mass (kg)']<= payload_mass[1]) ]
    # print(filtered_df.head(10))
    # print(payload_mass
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category'
        )
        return fig
    else:
        print("Entered the right site loop")
        # return the outcomes piechart for a selected site
        # fig = px.pie(data[data['Launch Site'] == entered_site], values='class', 
        filtered_df  = filtered_df[(filtered_df['Launch Site'] == entered_site)]
        print(filtered_df.head(10))
        print("We are here")
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
        color='Booster Version Category' 
        )
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
