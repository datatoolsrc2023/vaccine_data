# import os

from dagster import Definitions

from .assets import vaccine_assets
# from .jobs import TK
# from .resources import RESOURCES_LOCAL, RESOURCES_PROD, RESOURCES_STAGING
# from .sensors import make_slack_on_failure_sensor

all_assets = [*vaccine_assets]

'''
resources_by_deployment_name = {
    "prod": RESOURCES_PROD,
    "staging": RESOURCES_STAGING,
    "local": RESOURCES_LOCAL,
}
'''

# deployment_name = os.environ.get("DAGSTER_DEPLOYMENT", "local")

# all_sensors = [activity_analytics_assets_sensor, recommender_assets_sensor]
'''
if deployment_name in ["prod", "staging"]:
    all_sensors.append(make_slack_on_failure_sensor(base_url="my_dagit_url"))
'''

defs = Definitions(
    assets=all_assets,
    # resources=resources_by_deployment_name[deployment_name],
    # sensors=all_sensors,
)
