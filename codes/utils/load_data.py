import tqdm
import numpy as np
import pandas as pd

def load_metro_station_list(excel_path, time_status=None):
    '''
    line_info (pandas.DataFrame)
        metadata information of the metro lines
    time_status (None, str in {'current', 'all'})
    '''
    if time_status is None:
        time_status = 'current'

    # load metainfo of the metro lines
    line_info = pd.read_excel(excel_path, sheet_name='line_info')


    data_all = []

    for ix, row in tqdm.tqdm(line_info.iterrows(), desc='Loading data'):

        sn = row['sheet_name']
        ln = row['line_name']

        # print(f'Loading data for {ln}')

        # load data from excel
        data = pd.read_excel(excel_path, sheet_name=sn,
                             dtype={'no' : int, 'opening_data' : str}) \
                 .assign(line_name = ln,
                         line_name_zh = row['line_name_zh'],
                         line_color = row['color'],
                         line_cycle = row['cycle'])

        # time status
        if time_status in ['current']:
            data = data.query('opening_date != "u/c"')
            data = data.assign(opening_date = lambda x : pd.to_datetime(x['opening_date']))
        elif time_status in ['all']:
            # Check integrity of "date" columns
            pd.to_datetime(data.query('opening_date != "u/c"')['opening_date'])

        # append data
        data_all.append(data)

    # merge all date
    data = pd.concat(data_all, axis=0, ignore_index=True) \
             .astype({'line_cycle' : bool})

    return data
# =============================================================================