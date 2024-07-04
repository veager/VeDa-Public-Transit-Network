import re
import requests
import pandas as pd
from bs4 import BeautifulSoup


def ReqTrainStaList():
    '''
    Request train station list from LTA
    https://www.lta.gov.sg/content/ltagov/en/map/train.html
    '''
    
    import time
    
    url_li = [
        'https://www.lta.gov.sg/map/mrt/EWL/station_list.html',  # East-West Line
        'https://www.lta.gov.sg/map/mrt/NSL/station_list.html',  # North-South Line
        'https://www.lta.gov.sg/map/mrt/NEL/station_list.html',  # North East Line
        'https://www.lta.gov.sg/map/mrt/CCL/station_list.html',  # Circle Line
        'https://www.lta.gov.sg/map/mrt/DTL/station_list.html',  # Downtown Line
        'https://www.lta.gov.sg/map/mrt/TEL/station_list.html',  # Thomson-East Coast Line
        'https://www.lta.gov.sg/map/mrt/BPL/station_list.html',  # Bukit Panjang LRT
        'https://www.lta.gov.sg/map/mrt/STL/station_list.html',  # Sengkang LRT
        'https://www.lta.gov.sg/map/mrt/PTL/station_list.html'   # Punggol LRT
    ]
    
    station = pd.DataFrame(columns=['lne_n', 'stn_c', 'stn_n'])
    
    for url in url_li:
        time.sleep(2)
        html_doc = requests.get(url).text
        soup = BeautifulSoup(html_doc, 'html.parser')
        txt = soup.get_text()
        
        txt_li = txt.split('\n')
        txt_li = map(lambda x: x.strip(), txt_li)
        txt_li = list(filter(lambda x: len(x)!=0, txt_li))
        # print(len(txt_li))
        
        j = 1
        row = {}
        row['lne_n'] = txt_li[0]
        for i in range(4, len(txt_li), 2):
            row['stn_c'] = txt_li[i]
            row['stn_n'] = txt_li[i+1]
            j = j + 1
            station = station.append(row, ignore_index=True)
    return station
# ----------------------------------------------------------------------------


station = ReqTrainStaList()
station.to_csv('train_station_list.csv', index=False)
