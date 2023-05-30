import polars as pl
import datetime
import requests
from prefect import flow, task
from prefect.tasks import task_input_hash
from local_tasks.utils import PostgresCreds

# Program Purpose: pull state and city info from NIH surveys
# STEPS:
# 1. connect to NIH survey database
# 2. select state, city, years
# 3. convert to 

# database connection setup
pgc = PostgresCreds()

# run sql file
survey_count = open('local_tasks/extract/Census/pre.sql', 'r').read()
# clean survey_count so it's readable by polars, including \n, and \ characters
survey_count = survey_count.replace('\n', ' ').replace(';', '')
survey_count = pl.read_database(survey_count, pgc.engine)
breakpoint()
years = survey_count.select('year')

# 2021_variables
url = 'https://api.census.gov/data/2021/acs/acs1/profile/variables.json'

# 2019_variables
url = 'https://api.census.gov/data/2019/acs/acs1/profile/variables.json'

@task(
    name='api URL',
      cache_key_fn=task_input_hash,
      cache_expiration=datetime.timedelta(hours=24)
)
def getApiUrl(year:str):
    return f'http://api.census.gov/data/{year}/acs/acs1/profile'

# https://api.census.gov/data/2019/acs/acs1/profile?get=*&for=principal%20city%20(or%20part):*&in=metropolitan%20statistical%20area/micropolitan%20statistical%20area:19820%20state%20(or%20part):26

    
# pull api data from getapiurl task, with parameter PRINCITY is chicago
@task(
    name='api data',
        cache_key_fn=task_input_hash,
        cache_expiration=datetime.timedelta(hours=24)
)
def getApiData(url:str, cities:list):
    response = requests.get(url, params={'get': '*', 
                                         'for': 'place:00428803',
                                         'in': 'state:17'})

file = 'data/Census/state-geocodes-v2021.xlsx'
data = pl.read_excel(file, xlsx2csv_options={'skiprows': 5})
breakpoint()
print(data)