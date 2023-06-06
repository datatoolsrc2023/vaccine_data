from dagster import load_assets_from_package_module

from . import vaccine_assets

VACCINE_ASSETS = "vaccine_assets"

vaccine_assets = load_assets_from_package_module(package_module=vaccine_assets)
