#  1. Useful Sources


- **Land Transport Guru:** [website](https://landtransportguru.net)

- **Bus**

  - Bus Route
  - Bus Stop
  - BusRouter SG: [website](https://busrouter.sg/), [github](https://github.com/cheeaun/busrouter-sg/)
  - Bus route data: [github](https://github.com/cheeaun/sgbusdata)



- **MRT**
    - **wikipedia:** [Mass Rapid Transit](en.wikipedia.org/wiki/Mass_Rapid_Transit_(Singapore))
    - **MRT Station List:** [LTA Transport Tools](lta.gov.sg/content/ltagov/en/map/train.html)
    - **MRT Map**: [LTA Rail Network](https://www.lta.gov.sg/content/ltagov/en/getting_around/public_transport/rail_network.html)
    - **MRT Map of Singapore:** [website](https://mrtmapsingapore.com/)


# 2. Bus System



# 3. MRT System

## 3.1 Evolution

- 31 January 2020: Thomson–East Coast line (TE), TE1~TE3
- 28 August 2021: Thomson–East Coast line (TE), TE4~TE9
- 13 November 2022: Thomson–East Coast line (TE), TE11~TE22

## 3.2 Transfer Stations

- **Tap Out** Transfer Station:
  - DT11-NS21 Newton
  - DT32-EW2 Tampines
  - BP6-DT1 Bukit Panjang

## 3.3 Geospatial Location

### (1) Location From DataMall static data

Download from DataMall static data, [website](https://datamall.lta.gov.sg/content/dam/datamall/datasets/Geospatial/TrainStation.zip)

- Issues:
  - lose some stations : *BP14*, *CG*
    - Station *CG* is identical to Station *EW4*
  - The same name station in different lines (i.e., transfer station) has different coordinates

### (2) Location From citylines

preferred

### (3)  Location From Onemap API




## 3.4 Line Codes

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