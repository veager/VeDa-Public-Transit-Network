import time
import tqdm
import requests

def address_search(search_val):

    params = {
        'searchVal': search_val,
        'returnGeom': 'Y',
        'getAddrDetails': 'Y',
        'pageNum': 1}

    url = "https://www.onemap.gov.sg/api/common/elastic/search"

    req = requests.get(url, params=params)
    res = req.json()

    return res
# =============================================================
def request_address_from_list(search_list, sleep_time=0.1):

    data_all = []

    for search_val in tqdm.tqdm(search_list, desc='Requesting data'):

        time.sleep(sleep_time)

        try:
            res = address_search(search_val)
            res = res['results'][0]
            data_all.append(res)
        except:
            print('Failed request for:', search_val)

    return data_all
# =============================================================