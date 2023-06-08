# from dagster import asset, Definitions, ConfigurableResource
# import requests
# from requests import Response

# class MyConnectionResource(ConfigurableResource):
#     username: str

#     def request(self, endpoint: str) -> Response:
#         return requests.get(
#             f"https://my-api.com/{endpoint}",
#             headers={"user-agent": "dagster"},
#         )

# @asset
# def data_from_service(my_conn: MyConnectionResource) -> Dict[str, Any]:
#     return my_conn.request("/fetch_data").json()

# defs = Definitions(
#     assets=[data_from_service],
#     resources={
#         "my_conn": MyConnectionResource(username="my_user"),
#     },
# )

import os
from collections import defaultdict
import requests
import pandas as pd


class Utilities():
    def __init__(self):
        self.cities = ('Chicago city', 'New York city')

    # cities used in analysis
    def setCities(self, cities:list) -> list:
        self.cities = cities

class FIPSRecources():
    utils = Utilities()
    
    def __init__(self):
        self.data_path = '/Users/blakevanfleteren/Programs/GitHub/vaccine_data/vaccines/data'

    # determine years to pull data for
    def files(self) -> list:
        path = f'{self.data_path}/NIH_child/NIH_raw' # update from handcoded
        files = os.listdir(path)
        files = [file for file in files if file.endswith('.DAT')]
        return files

    # create list of years
    def years(self, files) -> list:
        years = [file.split('.')[0] for file in files]
        years = [f'20{year[6:8]}' for year in years]
        return years

    # pull FIPS data from census for each year
    def urls(self, years:list) -> dict:
        urls = defaultdict(dict)
        for year in years:
            state = f'https://www2.census.gov/programs-surveys/popest/geographies/{year}/state-geocodes-v{year}.xlsx'
            place = f'https://www2.census.gov/programs-surveys/popest/geographies/{year}/all-geocodes-v{year}.xlsx'
            urls.update({year: {'state': state, 'place': place}})
        return urls

    # pull FIPS Codes in excel format for each year
    def fipsFiles(self, urls:dict) -> list:
        cum_df = pd.DataFrame()
        for year, url in urls.items():
            place_url = url['place']
            response = requests.get(place_url)
            if response.status_code == 200:
                df = pd.read_excel(response.content, skiprows=4)
                df['year'] = year
                cum_df = pd.concat([cum_df, df])
                breakpoint()
        return cum_df
    
    # Full implementation of FIPS data pull
    def codes(self) -> pd.DataFrame:
        files = self.files()
        years = self.years(files)
        urls = self.urls(years)
        df = self.fipsFiles(urls)
        return df

class ACSResources():
    pass