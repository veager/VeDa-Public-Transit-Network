import re

import tqdm
import numpy as np
import pandas as pd


def _apply_location_cols(s):

    loc = s['location_gcj02']

    try:
        x = float(loc.split(',')[0])
        y = float(loc.split(',')[1])
    except:
        x = np.nan
        y = np.nan

    return x, y
# ---------------------------------------------------------------------------------------------


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

        # process "name"
        data['name'] = data['name'].str.replace(re.compile('\W'), '', regex=True) \
                                   .str.lower()

        # time status
        if time_status in ['current']:
            data = data.query('opening_date != "u/c"')
            data = data.assign(opening_date = lambda x : pd.to_datetime(x['opening_date']))
        elif time_status in ['all']:
            # Check integrity of "date" columns
            pd.to_datetime(data.query('opening_date != "u/c"')['opening_date'])

        # location information
        if 'location_gcj02' in data.columns.to_list():
            data[['x_gcj02', 'y_gcj02']] = data.apply(_apply_location_cols, axis=1, result_type='expand')

        # append data
        data_all.append(data)

    # merge all date
    data = pd.concat(data_all, axis=0, ignore_index=True) \
             .astype({'line_cycle' : bool})

    return data
# =============================================================================
def load_metro_station_list_v1(excel_path, time_status=None):
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
    for ix, row in tqdm.tqdm(line_info.iterrows(), desc='Loading data...'):

        sn = row['sheet_name']
        # print(f'Loading data for {ln}')

        # load data from excel
        data = pd.read_excel(
            excel_path, sheet_name=sn,
            dtype={'no' : int, 'opening_data' : str}) \
            .assign(sheet_name = sn) \
            .merge(line_info, on='sheet_name', how='left')
        # append data
        data_all.append(data)

    # merge all date
    data = pd.concat(data_all, axis=0, ignore_index=True)

    return data
# =====================================================================================================
def preprocess_metro_station(data, time_status=None):

    # processing station name, use as unique id
    # \W: any character that is not a letter, digit, or underscore ("_")
    data['name_id'] = data['station_name'].str.replace(re.compile('\W'), '', regex=True).str.lower()

    # closed date
    if 'closed_date' in data.columns.to_list():
        data['closed_date'] = data['closed_date'].infer_objects(copy=True).fillna(pd.Timestamp.max)
        data['closed_date'] = pd.to_datetime(data['closed_date'])
    else:
        data['closed_date'] = pd.Timestamp.max

    # time status
    if time_status == 'all':
        # Check integrity of "date" columns
        pd.to_datetime(data.query('opening_date != "u/c"')['opening_date'])
    else:
        if time_status == 'current':
            time_status = pd.to_datetime('now')
        else:
            time_status = pd.to_datetime(time_status)
        # Remove the uncompleted metro station
        data = data.query('opening_date != "u/c"')
        data = data.assign(opening_date = lambda x : pd.to_datetime(x['opening_date']))
        # Remove the closed metro station
        data = data.query('opening_date < @time_status') \
            .query('closed_date > @time_status')

    return data
# =====================================================================================================
