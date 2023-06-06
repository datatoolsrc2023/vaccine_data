import polars as pl
import pandas as pd
import os
import requests
from dagster import asset, Output, get_dagster_logger
from collections import defaultdict

logger = get_dagster_logger()

@asset(
    group_name='utils'
)
def cities() -> tuple:
    cities = (
        'Chicago city',
        'New York city')
    return cities

# determine years to pull data for
@asset(
    group_name='FIPS',
)
def files() -> list:
    path = 'data/NIH_child/NIH_raw' # update from handcoded
    files = os.listdir(path)
    files = [file for file in files if file.endswith('.DAT')]
    return files

@asset(
    group_name='utils'
)
def years(files:list) -> list:
    years = [file.split('.')[0] for file in files]
    years = [f'20{year[6:8]}' for year in years]
    return years

# pull FIPS data from census for each year
@asset(
    group_name='FIPS',
)
def urls(years:list) -> Output[dict]:
    urls = defaultdict(dict)
    for year in years:
        state = f'https://www2.census.gov/programs-surveys/popest/geographies/{year}/state-geocodes-v{year}.xlsx'
        place = f'https://www2.census.gov/programs-surveys/popest/geographies/{year}/all-geocodes-v{year}.xlsx'
        urls.update({year: {'state': state, 'place': place}})
    return Output(
        value=urls,
        metadata={
            year: urls[year] for year in years
        }
    )

# pull FIPS Codes in excel format for each year
@asset(
    group_name='FIPS',
)
def fipsFiles(urls:dict) -> list:
    for year, url in urls.items():
        place_url = url['place']
        path = 'data/Census/Census_raw' # update from handcoded
        response = requests.get(place_url)
        excel_path = f'{path}/{year}_FIPS_place.xlsx'
        directory = os.path.dirname(excel_path)
        os.makedirs(directory, exist_ok=True)
        with open(excel_path, 'wb') as file:
            file.write(response.content)
        pd.read_excel(
            excel_path, 
            skiprows=4,
            engine='openpyxl',
            ).to_csv(f'{path}/{year}_FIPS_place.csv', index=False)
    files = os.listdir(path)
    # update to more specific search criteria
    return [f'{path}/{file}' for file in files if file.startswith('20')]  

# identify FIPS for Chicago, IL and New York, NY
@asset(
    group_name='FIPS',
)
def fipsLocation(years:list, cities:tuple) -> dict:
    fips = defaultdict(list)
    for year in years:
        file = f'data/Census/Census_raw/{year}_FIPS_place.csv' # update from handcoded
        for city in cities:
            fips[year].append(str(pl.read_csv(file)
                        .select(name=pl.col('^Area Name.*$')
                        .where(pl.col('^Area Name.*$') == city)
                        .limit(1)).to_series()[0]))
    return fips

# pull American Community Survey variables for each year
@asset(
    group_name='ACS',
)
def acsVars(years:list) -> dict:
    variables = {}
    for year in years:
        url = f'https://api.census.gov/data/{year}/acs/acs1/subject/variables.json'
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            variables[year] = response.json()['variables']
        else:
            logger.error(f'Error with {year}: {response.status_code}')
    return variables


# pull American Community Survey data for each year
@asset(
    group_name='ACS',
)
def acsURLs(years:list, fipsLocation:dict, acsVars:dict) -> dict:
    urls = defaultdict(list)
    for year in acsVars.keys():
        cities = fipsLocation[year]
        for city in cities:
            key = 'cc1e68d7a1e08032441b961b0264d57bcfab83bb'
            vars = ','.join(var for var in acsVars[year].keys())
            url = f'https://api.census.gov/data/{year}/acs/acs1/cprofile?get={vars}&for=place:{city}&key={key}'
            url = url.replace(' ', '%20')
            urls[year].append(url)
    return urls

# pull American Community Survey data for each year
@asset(
    group_name='ACS',
)
def acsData(acsURLs:dict) -> dict:
    data = defaultdict(list)
    for year, urls in acsURLs.items():
        for url in urls:
            response = requests.get(url)
            data[year].append(response.json())
    return data