from dagster import job
from ops.extract import (
    getFiles,
    getYears,
    setURLs,
    pullFIPS,
)


# extract FIPS files
@job
def extractFIPS():
    files = getFiles()
    years = getYears(files)
    urls = setURLs(years)
    pullFIPS(urls)