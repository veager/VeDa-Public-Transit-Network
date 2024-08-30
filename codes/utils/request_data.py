import json
import time
import copy
import datetime
import requests

import tqdm
import pandas as pd



def geocoding(search_value, city='', key=None):

    url = 'https://restapi.amap.com/v3/geocode/geo'

    params = {'address' : search_value,
              'city'    : city,
              'output'  : 'json',
              'key'     : key}

    time.sleep(0.05)
    res = requests.get(url, params=params)

    if res.status_code != 200:
        print('URL Request Failed, statue code:', search_value, res.status_code)
        data = [{'search_value' : search_value}]
        return data

    res = res.text
    res = json.loads(res)

    if int(res['status']) != 1:
        print('Request Failes', search_value, res)
        data = [{'search_value' : search_value}]
        return data

    data_all = []

    # Successful Request
    for i in range(int(res['count'])):
        address = {}

        address['search_value']      = search_value
        address['formatted_address'] = str(res['geocodes'][i].get('formatted_address', ''))
        address['country']           = str(res['geocodes'][i].get('country', ''))
        address['province']          = str(res['geocodes'][i].get('province', ''))
        address['city']              = str(res['geocodes'][i].get('city', ''))
        address['citycode']          = str(res['geocodes'][i].get('citycode', ''))
        address['district']          = str(res['geocodes'][i].get('district', ''))
        address['adcode']            = str(res['geocodes'][i].get('adcode', ''))
        address['location']          = str(res['geocodes'][i].get('location', ''))
        address['level']             = str(res['geocodes'][i].get('level', ''))

        data_all.append(address)

    return data_all
# =============================================================