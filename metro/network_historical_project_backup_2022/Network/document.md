MRT Train Network

## 1. MRT Map

LTA Rail Network, [website](https://www.lta.gov.sg/content/ltagov/en/getting_around/public_transport/rail_network.html)

MRT Map of Singapore, [website](https://mrtmapsingapore.com/)

## 2. Raw Data

#### (1) TrainStation.zip

- Download from DataMall static data, [website](https://datamall.lta.gov.sg/content/dam/datamall/datasets/Geospatial/TrainStation.zip)
- Issues:
  - lose some stations : *BP14*, *CG*
    - Station *CG* is identical to Station *EW4*
  - The same name station in different lines (i.e., transfer station) has different coordinates

#### (2) MRT-Station-Codes.csv

- Download from DataMall static data: [Train Station Codes and Chinese Names](https://datamall.lta.gov.sg/content/dam/datamall/datasets/PublicTransportRelated/Train_Station_Codes_and_Chinese_Names.zip)

- Corrected manually

  - adjust *line name*s according to `MRT-Line-Codes.csv`

  - add closed stations information

- Format

  - Stations is listed **in sequential order** for each line

- **Not** contain the last line segment of the the loop line. The **last line segment** information is presented in `MRT-Loop-Line-Complement.csv`.
  - The same name stations in different lines share the **same** *station name* but have different *station code*s.
  
- The **interchange information** for the stations will be presented in `MRT-Transfer-Stations.csv`

#### (3) MRT-Loop-Line-Complement.csv

- Created manually

- The **last line segments** information of **loop lines**, including:

    - Punggol LRT East Loop (PEL)

    - Punggol LRT West Loop (PWL)

    - Sengkang LRT East Loop (SEL) 

    - Sengkang LRT West Loop (SWL)

    - Bukit Panjang LRT (BPL)

#### (4) MRT-Line-Codes.csv

- Download from DataMall static data: [Train Lines Codes](https://datamall.lta.gov.sg/content/dam/datamall/datasets/PublicTransportRelated/Train%20Line%20Codes.zip)
- With minor adjustments

| line_code | line_name               |
| :-------: | ----------------------- |
|    CCL    | Circle Line             |
|    CEL    | Circle Line Extension   |
|    CGL    | Changi Extension        |
|    DTL    | Downtown Line           |
|    EWL    | East West Line          |
|    NEL    | North East Line         |
|    NSL    | North South Line        |
|    TEL    | Thomson-East Coast Line |
|    PEL    | Punggol LRT East Loop   |
|    PWL    | Punggol LRT West Loop   |
|    SEL    | Sengkang LRT East Loop  |
|    SWL    | Sengkang LRT West Loop  |
|    BPL    | Bukit Panjang LRT       |

#### (5) MRT-Transfer-Stations-Raw.csv

- Data collected from: [MRT stations in Singapore](https://mrtmapsingapore.com/mrt-stations-singapore/)

- Quite similarly to `MRT-Line-Codes.csv`, but all *station code*s for a station will be presented. 

#### (6) MRT-Transfer-Stations.csv

- Extracted from `MRT-Transfer-Stations-Raw.csv`
- drop duplicated data, thus, keep the *station code*s be unique.

## 3. Closed Stations

- **Ten Mile Junction Station (BP14)** of the **Bukit Panjang LRT Line** is closed from 13 January 2019
  
  - *TrainStation.zip* data doesn't include this station
  
- **Hume Station (DT4)** of **Downtown Line (DTL)** is closed from 7 March 2019 and is planned to be open by 2025. [wikipedia](https://en.wikipedia.org/wiki/Hume_MRT_station)

- **Bukit Brown Station (CC18)** of **Circle line (CCL)**. [wikipedia](https://en.wikipedia.org/wiki/Bukit_Brown_MRT_station)

- **Teck Lee LRT Station (PW2)** of the **Bukit Panjang West LRT Line** is not in service.

## 4. Limitations

- not include the geographical length of line segments
- not contain the geographical topology of line segments

