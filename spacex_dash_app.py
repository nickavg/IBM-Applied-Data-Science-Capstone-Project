import pandas as pd
import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
spacex_df = pd.read_csv("spacex_launch_dash.csv")
L_Sites_list=spacex_df['Launch Site'].unique().tolist()
Class_list=spacex_df['class'].unique().tolist()
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
spacex_df = spacex_df[['Launch Site', 'class', 'Payload Mass (kg)', 'Booster Version Category']]
spacex_df_0 = spacex_df[spacex_df['Launch Site']==L_Sites_list[0]]
spacex_df_1 = spacex_df[spacex_df['Launch Site']==L_Sites_list[1]]
spacex_df_2 = spacex_df[spacex_df['Launch Site']==L_Sites_list[2]]
spacex_df_3 = spacex_df[spacex_df['Launch Site']==L_Sites_list[3]]
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
            dcc.Dropdown(id='site-dropdown', options=[
                    {'label': 'All Sites', 'value': 'ALL'},
                    {'label': L_Sites_list[0], 'value': L_Sites_list[0]},
                    {'label': L_Sites_list[1], 'value': L_Sites_list[1]},
                    {'label': L_Sites_list[2], 'value': L_Sites_list[2]},
                    {'label': L_Sites_list[3], 'value': L_Sites_list[3]}],
                value='ALL',
                placeholder="Select a Launch Site here",
                searchable=True
                ),
            html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
            html.Div(dcc.Graph(id='success-pie-chart')),
            html.Br(),
            html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
            html.Div(dcc.RangeSlider(id='payload-slider',
                min=0, max=10000, step=1000, marks={0: '0', 2000: '2,000', 4000: '4,000', 6000: '6,000', 8000: '8,000', 10000: '10,000'}, value=[min_payload, max_payload])),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
            html.Div(dcc.Graph(id='success-payload-scatter-chart'))])
# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
# CALLBACK 1  CALLBACK 1  CALLBACK 1  CALLBACK 1  CALLBACK 1  CALLBACK 1  CALLBACK 1 
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches by Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        fig = px.pie(filtered_df, names='class', 
        title=('Total Success Launches for site %s' % entered_site))
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs,
# `success-payload-scatter-chart` as output
# CALLBACK 2  CALLBACK 2 CALLBACK 2 CALLBACK 2 CALLBACK 2 CALLBACK 2 CALLBACK 2 CALLBACK 2 CALLBACK 2 CALLBACK 2
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site,value):
    spacex_pl_df = spacex_df[spacex_df['Payload Mass (kg)'].between(value[0], value[1], inclusive=True)]
    filtered_ls_df = spacex_df[spacex_df['Launch Site']==entered_site]
    filtered_pm_df = filtered_ls_df[filtered_ls_df['Payload Mass (kg)'].between(value[0], value[1], inclusive=True)]
    #count_class1 = filtered_pm_df['class'].sum()
    #count_class2 = filtered_ls_df['class'].sum()
    if entered_site == 'ALL':
        fig = px.scatter(spacex_pl_df, x='Payload Mass (kg)', 
        y='class', color='Booster Version Category',
        title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        fig = px.scatter(filtered_pm_df, x='Payload Mass (kg)',
        y='class', color='Booster Version Category',
        title=('Payload and Booster versions for site %s' % entered_site))
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
