import polars as pl
import pandas as pd
import os
import requests
from dagster import asset, Output, get_dagster_logger
from collections import defaultdict

logger = get_dagster_logger()

@asset(
    group_name='FIPS',
    io_manager_key='bigquery_io_manager',
    required_resource_keys={'fips'},
)
def fipsCodes(context):
    fips = context.resources.fips.codes()
    return fips

# identify FIPS for Chicago, IL and New York, NY
@asset(
    group_name='FIPS',
    io_manager_key='bigquery_io_manager',
    required_resource_keys={'fips'},
)
def fipsLocation(context, df:pd.DataFrame) -> dict:
    cities = context.resources.fips.utils.cities()
    df = (pl.from_pandas(df)
          .filter(df['city'].isin(cities))
          .select(name = pl.col('^Area_Name.*'))
          .to_pandas())
    return df

# pull American Community Survey variables for each year
@asset(
    group_name='ACS',
    io_manager_key='bigquery_io_manager',
)
def acsVars(context) -> dict:
    variables = {}
    years = context.resources.fips.utils.years()
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
    io_manager_key='bigquery_io_manager',
)
def acsURLs(fipsLocation:dict, acsVars:dict) -> dict:
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
    io_manager_key='bigquery_io_manager',
)
def acsData(acsURLs:dict) -> dict:
    data = defaultdict(list)
    for year, urls in acsURLs.items():
        for url in urls:
            response = requests.get(url)
            data[year].append(response.json())
    return data