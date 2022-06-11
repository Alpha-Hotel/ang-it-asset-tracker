from numpy import dtype
import pandas as pd
import datetime as dt

test_flag = True

if test_flag == False:

    df = pd.read_excel(
        'C:/Users/ahpar/Desktop/DoD SAFE-HopvceRgWUpfyQ9N/DoD SAFE-HopvceRgWUpfyQ9N/ang-it-asset-tracker/Raw Data.xls', sheet_name=None, header=None)
    column_names = df['Sheet1'].loc[[0]]

else:
    ''
    df = {
        'Sheet1': pd.DataFrame({
            '1': ['Last Inv Dt/Tm', '2022-04-29', '2022-05-29'],
            '2': ['UIC', 'FA706', 'FA489']
        })}
    print(df)
    column_names = df['Sheet1'].loc[[0]]

data = pd.DataFrame()
Unit_Total_Assets = {}
Unit_Completed_Assets = {}


print(column_names.values)

for i in df.keys():
    ''
    df[i].columns = column_names.values[0]
    data = pd.concat([data.reset_index(drop=True),
                     df[i].reset_index(drop=True)], axis=0)

data = data.dropna(how='all')
data = data.iloc[1:, :]
data = data.reset_index(drop=True)
# Set to date/time dtype
data['Last Inv Dt/Tm'] = pd.to_datetime(data['Last Inv Dt/Tm'])

#   Get Unit Names  #
Unit_Names = data['UIC'].drop_duplicates(keep='first', inplace=False)
print(Unit_Names)
print(data.dtypes)

# Get completion stats
for i in Unit_Names:
    Unit_Total_Assets[i] = data.loc[data['UIC'] == i].count
    Unit_Completed_Assets[i] = data.loc[data['UIC']
                                        == i & dt.datetime.now() - dt.timedelta(days=365) > dt.datetime.strptime(data['Last Inv Dt/Tm'], '%y-%m-%d %H:%M')]


print('Assets by unit  : \n', Unit_Total_Assets,
      '\n\n', Unit_Completed_Assets, '\n\n')

print(data.info)
