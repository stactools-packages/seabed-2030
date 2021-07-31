from datetime import datetime
import re
import logging

from pystac import (
    Collection,
    Item,
    Asset,
    Extent,
    SpatialExtent,
    TemporalExtent,
    CatalogType,
    MediaType,
)
from pystac.extensions.projection import ProjectionExtension

from stactools.seabed_2030.constants import (
    SEABED_2030_ID,
    SPATIAL_EXTENT,
    TEMPORAL_EXTENT,
    SEABED_PROVIDER,
    TITLE,
    DESCRIPTION,
    LICENSE,
    SEABED_EPSG,
)

from netCDF4 import Dataset

logger = logging.getLogger(__name__)


def create_collection() -> Collection:
    """Create a STAC Collection for Seabed-2030 Bathymetric Data

    This dataset currently includes a single file that is updated regularly. To
    address possible changes to file metadata over time, the collection attributes
    are hard-coded in constants.py.

    Returns:
        Collection: STAC Collection object
    """
    extent = Extent(
        SpatialExtent([SPATIAL_EXTENT]),
        TemporalExtent(TEMPORAL_EXTENT),
    )

    collection = Collection(
        id=SEABED_2030_ID,
        title=TITLE,
        description=DESCRIPTION,
        license=LICENSE,
        providers=[SEABED_PROVIDER],
        extent=extent,
        catalog_type=CatalogType.RELATIVE_PUBLISHED,
    )

    return collection


def create_item(nc_href: str, cog_href: str) -> Item:
    """Create a STAC Item

    Collect metadata from a Seabed 2030 netcdf file to create the Item

    Args:
        nc_href (str): The HREF pointing to the GECBO grid netcdf file
        cog_href (str): The HREF pointing to the associated asset COG. The COG should
        be created in advance using `cog.create_cog`

    Returns:
        Item: STAC Item object
    """
    with Dataset(nc_href) as ds:
        properties = {
            "title": ds.title,
            "institution": ds.institution,
            "source": ds.source,
            "history": ds.history,
            "comment": ds.comment,
        }

        dims = ds.dimensions
        ds_shape = [dims["lon"].size, dims["lat"].size]
        x_cellsize = 360.0 / float(dims["lon"].size)
        y_cellsize = 180.0 / float(dims["lat"].size)

    global_geom = {
        "type":
        "Polygon",
        "coordinates": [[[-180.0, -90.0], [180.0, -90.0], [180.0, 90.0],
                         [-180.0, 90.0], [-180.0, -90.0]]],
    }

    try:
        item_year = re.findall(r"\d{4}", properties["title"])[0]
    except IndexError:
        raise ValueError(
            "Unable to obtain year from the dataset title attribute")

    item_datetime = datetime(int(item_year), 1, 1)

    item = Item(
        id=f"{SEABED_2030_ID}-gebco-{item_year}",
        properties=properties,
        geometry=global_geom,
        bbox=SPATIAL_EXTENT,
        datetime=item_datetime,
        stac_extensions=[],
    )

    proj_attrs = ProjectionExtension.ext(item, add_if_missing=True)
    proj_attrs.epsg = SEABED_EPSG
    proj_attrs.bbox = SPATIAL_EXTENT
    proj_attrs.shape = ds_shape
    proj_attrs.transform = [
        SPATIAL_EXTENT[0],
        x_cellsize,
        0.0,
        SPATIAL_EXTENT[1],
        0.0,
        -y_cellsize,
    ]

    # Add the COG asset
    item.add_asset(
        "image",
        Asset(
            href=cog_href,
            media_type=MediaType.COG,
            roles=["data"],
            title=properties["title"].replace("Grid", "COG"),
        ),
    )

    return item
