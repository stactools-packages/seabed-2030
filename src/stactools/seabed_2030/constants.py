from datetime import datetime

from pyproj import CRS
from pystac import Provider, ProviderRole, Link

SEABED_2030_ID = "seabed-2030"
SEABED_EPSG = 4326
SEABED_CRS = CRS.from_epsg(SEABED_EPSG)
LICENSE = "CC-BY-4.0"
THUMBNAIL = "https://seabed2030.org/sites/default/files/styles/card/public/images/news_image.jpg"
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
DESCRIPTION = (
    "GEBCO's gridded bathymetric datasets are a global terrain model" +
    " for ocean and land, providing elevation data, in meters, on a 15 arc-second interval grid."
)

# Scientific Citation extension
SEABED_DOI = "10.5285/c6612cbe-50b3-0cff-e053-6c86abc09f8f"
SEABED_CITATION = "GEBCO Compilation Group (2021) GEBCO 2021 Grid"
SEABED_CITE_AS = Link(
    rel="cite-as",
    target="https://www.gebco.net/data_and_products/gridded_bathymetry_data",
)

# Attribution collected from .nc file
INSTITUTION = "On behalf of the General Bathymetric Chart of the Oceans (GEBCO), the data are held at the British Oceanographic Data Centre (BODC)."  # noqa
SOURCE = "The GEBCO_2020 Grid is the latest global bathymetric product released by the General Bathymetric Chart of the Oceans (GEBCO) and has been developed through the Nippon Foundation-GEBCO Seabed 2030 Project. This is a collaborative project between the Nippon Foundation of Japan and GEBCO. The Seabed 2030 Project aims to bring together all available bathymetric data to produce the definitive map of the world ocean floor and make it available to all."  # noqa
HISTORY = "Information on the development of the data set and the source data sets included in the grid can be found in the data set documentation available from https://www.gebco.net"  # noqa
COMMENT = "The data in the GEBCO_2020 Grid should not be used for navigation or any purpose relating to safety at sea."  # noqa
