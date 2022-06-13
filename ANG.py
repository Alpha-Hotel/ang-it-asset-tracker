import numpy as np
import pandas as pd
import datetime as dt
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)


test_flag = True
print('----##### LOADING DATA ####----')
if test_flag == False:
    df = pd.read_excel(
        'C:/Users/ahpar/Desktop/DoD SAFE-HopvceRgWUpfyQ9N/ang-it-asset-tracker/Raw Data.xls', sheet_name=None, header=None)
    column_names = df['Sheet1'].loc[[0]]

else:
    df = {
        'Sheet1': pd.DataFrame({
            '1': ['Last Inv Dt/Tm', '2020-04-29', '2020-05-29', '2022-05-29', '2022-05-29', '2021-06-29', '2021-06-29', '2020-04-29'],
            '2': ['UIC', 'FA706', 'FA489', 'FA489', 'FA489', 'FA489', 'FA706', 'FA334'],
            '3': ['Loc', 'TX', 'AK', 'DE', 'MI', '', '', 'AK'],
            '4': ['Serial Number', '1234', '45677', '45678', '098765', '965769', '21412', '213']
        })}
    states_df = pd.DataFrame({

    })
    column_names = df['Sheet1'].loc[[0]]

print('----##### DATA LOADED ####----')
data = pd.DataFrame()
Unit_Total_Assets = {}
Unit_Completed_Assets = {}
Unit_Due_Inspections = {}
Unit_Percent_Complete = {}
Unit_Due_In_6 = {}

for i in df.keys():
    df[i].columns = column_names.values[0]
    data = pd.concat([data.reset_index(drop=True),
                     df[i].reset_index(drop=True)], axis=0)

#   Clean Data  #
data = data.dropna(how='all')
data = data.iloc[1:, :]
data = data.reset_index(drop=True)
# Set to date/time dtype
data['Last Inv Dt/Tm'] = pd.to_datetime(data['Last Inv Dt/Tm'])

#   Get Unit Names  #
Unit_Names = data['UIC'].drop_duplicates(keep='first', inplace=False)

# Get completion stats  #
Due_DF = data[dt.datetime.now() - dt.timedelta(days=365)
              > data['Last Inv Dt/Tm']]
Complete_DF = data[dt.datetime.now() - dt.timedelta(days=365)
                   < data['Last Inv Dt/Tm']]
Due_in_6 = data[(dt.datetime.now() - dt.timedelta(days=183)
                > data['Last Inv Dt/Tm']) & (dt.datetime.now() - dt.timedelta(days=360)
                < data['Last Inv Dt/Tm'])]

for i in Unit_Names:
    print('----##### GETTING DATA FOR {unit} ####----'.format(unit=i))
    Unit_Total_Assets[i] = data[data['UIC']
                                == i]
    Unit_Completed_Assets[i] = Complete_DF[(
        Complete_DF['UIC'] == i)]
    Unit_Due_Inspections[i] = Due_DF[(Due_DF['UIC'] == i)]
    Unit_Percent_Complete[i] = (
        Unit_Completed_Assets[i].shape[0]/Unit_Total_Assets[i].shape[0])*100
    Unit_Due_In_6[i] = Due_in_6[(Due_in_6['UIC'] == i)]

#   Print Output    #
output = pd.DataFrame({
    'Unit': [np.nan],
    'Unit Assets': [np.nan],
    'Completed Inspections': [np.nan],
    'Inspections Due': [np.nan],
    'Completion Percentage': [np.nan],
    'Due in the Next 6 Monts': [np.nan],
    'State': [np.nan],
    'Greater Than 6': [np.nan]
})

for i in Unit_Names:
    print('{Unit}\nUnit Assets: \n{total}\nCompleted Inspections:\n{complete}\nUnit Inspections Due:\n{due}\nUnit Inspection Completion Percentage:\n{p}%\nUnit # Inspections Coming Due in Next 6 Months\n{sixm}\n'.format(
        Unit=i, total=Unit_Total_Assets[i].shape[0],
        complete=Unit_Completed_Assets[i].shape[0],
        due=Unit_Due_Inspections[i].shape[0],
        p=Unit_Percent_Complete[i],
        sixm=Unit_Due_In_6[i].shape[0]
    ))
    output = pd.concat([output, pd.DataFrame({
        'Unit': [i],
        'Unit Assets': [Unit_Total_Assets[i].shape[0]],
        'Completed Inspections': [Unit_Completed_Assets[i].shape[0]],
        'Inspections Due': [Unit_Due_Inspections[i].shape[0]],
        'Inspection Percentage': [int(Unit_Percent_Complete[i])],
        'Due in 6': [Unit_Due_In_6[i].shape[0]],
        'Greater than 6':[(Unit_Completed_Assets[i].shape[0]-Unit_Due_In_6[i].shape[0])],
        'State': [np.nan]
    })])


output = output.reset_index(drop=True)
output = output.dropna(how='all')
output.to_csv('out.csv', index=False)

#   Make Figures    #
app_options = pd.concat([Unit_Names, pd.Series(['All Units'])])

app.layout = html.Div([
    html.H4('Inspection Health by Unit'),
    dcc.Dropdown(
        id="bardropdown",
        options=['Grouped', 'Stacked'],
        value="Grouped",
        clearable=False,
    ),
    dcc.Dropdown(
        id="dropdown",
        options=app_options,
        value=Unit_Names[0],
        clearable=False,
    ),
    dcc.Graph(id="graph"),
    html.H4('Overall Inspection Health'),
    dcc.Graph(id="pie"),
    html.H4("Percentage of Complete Inspections"),
    dcc.Graph(id='scatter')
])


@ app.callback(
    Output("graph", "figure"),
    Input("dropdown", "value"),
    Input("bardropdown", "value"))
def update_bar_chart(Unit, graph_type):
    if Unit == 'All Units':
        mask = pd.Series(True, index=output['Unit'].index)
    else:
        mask = output['Unit'] == Unit

    print(graph_type)
    # Group Bar chart
    if graph_type == "Grouped":
        fig = px.bar(output[mask], x="Unit", y=[
            'Greater than 6', 'Due in 6', 'Inspections Due'],
            barmode="group", color_discrete_sequence=["DarkGreen", "Goldenrod", "FireBrick"], text_auto=True)
    else:
        fig = px.bar(output[mask], x="Unit", y=[
            'Greater than 6', 'Due in 6', 'Inspections Due'], color_discrete_sequence=["DarkGreen", "Goldenrod", "FireBrick"], title="Long-Form Input")

    return fig


'''pie_values = pd.DataFrame({'values': [
    output['Greater than 6'].sum(), output['Due in 6'].sum(),
    output['Inspections Due'].sum()]})
'''
pie_values = pd.DataFrame({'values': [
    6, 2, 3
]})


print(pie_values)


@app.callback(
    Output("pie", "figure"),
    Input("dropdown", "value"))
def generate_chart(Unit):
    fig = px.pie(pie_values, values='values', names=[
        'Greater than 6', 'Due in 6', 'Inspections Due'], color_discrete_sequence=["DarkGreen", "Goldenrod", "FireBrick"], hole=.3)
    return fig


@app.callback(
    Output("scatter", "figure"),
    Input("dropdown", "value")
)
def generate_scatter(value):
    mask = pd.Series(True, index=output['Unit'].index)
    fig = px.scatter(output[mask], x="Unit", y="Inspection Percentage")
    return fig


app.run_server(debug=True)
