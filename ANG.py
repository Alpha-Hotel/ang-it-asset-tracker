import numpy as np
import pandas as pd
import datetime as dt

test_flag = True
print('----##### LOADING DATA ####----')
if test_flag == False:
    df = pd.read_excel(
        'C:/Users/ahpar/Desktop/DoD SAFE-HopvceRgWUpfyQ9N/ang-it-asset-tracker/Raw Data.xls', sheet_name=None, header=None)
    column_names = df['Sheet1'].loc[[0]]

else:
    df = {
        'Sheet1': pd.DataFrame({
            '1': ['Last Inv Dt/Tm', '2020-04-29', '2020-05-29', '2022-05-29', '2022-05-29', '2021-06-29'],
            '2': ['UIC', 'FA706', 'FA489', 'FA489', 'FA489', 'FA489'],
            '3': ['Loc', 'TX', 'AK', 'DE', 'MI', ''],
            '4': ['Serial Number', '1234', '45677', '45678', '098765', '965769']
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
    'Inspection Percentage': [np.nan],
    'Due in 6': [np.nan]
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
        'Due in 6': [Unit_Due_In_6[i].shape[0]]
    })])


output = output.reset_index(drop=True)

print(output.to_csv('out.csv', index=False))
