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

class FipsRecources():
    utils = Utilities()
    
    def __init__(self):
        pass

    # determine years to pull data for
    def files(self) -> list:
        path = 'data/NIH_child/NIH_raw' # update from handcoded
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