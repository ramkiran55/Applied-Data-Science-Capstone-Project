# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
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
                                dcc.Dropdown(id='site-dropdown',options=[
                                    {'label':'ALL SITES','value':'ALL SITES'},
                                    {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'},
                                    {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                    {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},
                                    {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                ],
                                value='ALL SITES',
                                placeholder='Select a Launch Site here',
                                searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min=0,
                                max=10000,
                                step=1000,
                                value=[min_payload,max_payload]
                                ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def pie(site_dropdown):
    if site_dropdown == 'ALL SITES':
        title_pie = f"Success Launches for {site_dropdown}"       
        fig = px.pie(spacex_df, values='class', names='Launch Site', title=title_pie)
        return fig
    else:
        filtered_DD= spacex_df[spacex_df['Launch Site'] == site_dropdown]
        filtered_LS = filtered_DD.groupby(['Launch Site','class']).size().reset_index(name='class count')
        title_pie = f"Success Launches for site {site_dropdown}"       
        fig = px.pie(filtered_LS, values='class count', names='class', title=title_pie)
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])

def build_scatter(site_dropdown,slider_range):
    #Taking Range in here
    low, high = slider_range
    #Selecting values between slider range
    mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    #Getting the filtered dataFrame
    filtered_df = spacex_df[mask]
    
    #If we are showing all the sites
    if site_dropdown == 'ALL SITES':
        #Display all values for the variable
        fig = px.scatter(filtered_df,x="Payload Mass (kg)", y="class", color="Booster Version Category", title='Payload vs. Outcome for All Sites')
        return fig
    else:
        print(site_dropdown)
        filtered_df1= filtered_df[filtered_df['Launch Site'] == site_dropdown]
        fig = px.scatter(filtered_df1, x="Payload Mass (kg)", y="class", color="Booster Version Category", title=f'Payload vs. Outcome for {site_dropdown}')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
