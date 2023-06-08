# __init__.py
from dagster_gcp_pandas import BigQueryPandasIOManager

from dagster import Definitions
from .assets import (cities, files, years,
                     urls, fipsFiles, acsVars,
                     acsData, acsURLs, fipsLocation)
import os

# Note that storing passwords in configuration is bad practice. It will be resolved later in the guide.
resources = {
    "blake_dev": {
        "bigquery_io_manager": BigQueryPandasIOManager(
            project="sonic-ivy-388314",
            dataset="vaccinedata_blake_dev",
            timeout=15.0
        ),
        "data_storage": "vaccinedata_blake_dev",
    },    
    "nikki_dev": {
        "bigquery_io_manager": BigQueryPandasIOManager(
            project="sonic-ivy-388314",
            dataset="vaccinedata_nikki_dev",
            timeout=15.0
        ),
        "data_storage": "vaccinedata_nikki_dev"
    },
    "production": {
        "bigquery_io_manager": BigQueryPandasIOManager(
            project="sonic-ivy-388314",
            dataset="vaccinedata",
            timeout=15.0
        ),
        "data_storage": "vaccinedata",
    },
}

deployment_name = os.getenv("DAGSTER_DEPLOYMENT", "blake_dev")

defs = Definitions(
    assets=[cities, files, years, urls, fipsFiles, fipsLocation,
                    acsVars, acsData, acsURLs], resources=resources[deployment_name]
)
