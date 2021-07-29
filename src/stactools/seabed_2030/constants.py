from datetime import datetime

from pyproj import CRS
from pystac import Provider, ProviderRole

SEABED_2030_ID = "seabed-2030"
SEABED_EPSG = 4326
SEABED_CRS = CRS.from_epsg(SEABED_EPSG)
LICENSE = "CC-BY-4.0"
SPATIAL_EXTENT = [-180.0, 90.0, 180.0, -90.0]
# The first grid was released in 2003, and Items will provide additional
# temporal information as they are created
TEMPORAL_EXTENT = [
    datetime(2003, 1, 1),
    None,
]
SEABED_PROVIDER = Provider(
    name="GEBCO Compilation Group",
    roles=[ProviderRole.PRODUCER, ProviderRole.PROCESSOR, ProviderRole.HOST],
    url="https://www.gebco.net/data_and_products/gridded_bathymetry_data/",
)
TITLE = "Seabed 2030 General Bathymetric Chart of the Oceans (GEBCO) Grid"
DESCRIPTION = "GEBCO's gridded bathymetric datasets are a global terrain model" \
    + " for ocean and land, providing elevation data, in meters, on a 15 arc-second interval grid."
