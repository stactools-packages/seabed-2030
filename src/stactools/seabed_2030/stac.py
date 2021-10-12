import os
from datetime import datetime
import re
import logging
from typing import Optional

import fsspec
from stactools.core.io import ReadHrefModifier
from pystac.extensions.scientific import ScientificExtension
import rasterio
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
from pystac.extensions.file import FileExtension
from pystac.extensions.item_assets import AssetDefinition, ItemAssetsExtension
from pystac.extensions.raster import (
    DataType,
    RasterBand,
    RasterExtension,
    Sampling,
)

from stactools.seabed_2030.constants import (
    SEABED_2030_ID,
    SPATIAL_EXTENT,
    TEMPORAL_EXTENT,
    THUMBNAIL,
    SEABED_PROVIDER,
    TITLE,
    DESCRIPTION,
    LICENSE,
    SEABED_EPSG,
    INSTITUTION,
    SOURCE,
    HISTORY,
    COMMENT,
    SEABED_DOI,
    SEABED_CITATION,
    SEABED_CITE_AS,
)

logger = logging.getLogger(__name__)


def create_collection(thumbnail_url: str = THUMBNAIL) -> Collection:
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

    collection.add_asset(
        "thumbnail",
        Asset(
            href=thumbnail_url,
            media_type=MediaType.JPEG,
            roles=["thumbnail"],
            title="Seabed 2030 thumbmail",
        ),
    )

    collection_proj = ProjectionExtension.summaries(collection,
                                                    add_if_missing=True)
    collection_proj.epsg = [SEABED_EPSG]

    collection_sci = ScientificExtension.ext(collection, True)
    collection_sci.apply(SEABED_DOI, SEABED_CITATION)

    collection.add_link(SEABED_CITE_AS)

    collection_item_asset = ItemAssetsExtension.ext(collection,
                                                    add_if_missing=True)
    collection_item_asset.item_assets = {
        "elevation":
        AssetDefinition({
            "type":
            MediaType.COG,
            "roles": ["data"],
            "title":
            "Seabed 2030 elevation",
            "raster:bands": [
                RasterBand.create(
                    nodata=-32767,
                    unit="masl",
                    sampling=Sampling.POINT,
                    data_type=DataType.INT16,
                    spatial_resolution=15 / 3600.0,
                ).to_dict()
            ],
            "proj:epsg":
            SEABED_EPSG,
        }),
    }

    return collection


def create_item(cog_href: str, cog_href_modifier: Optional[ReadHrefModifier] = None) -> Item:
    """Create a STAC Item

    Create an item for a corresponding COG, which may be the entire area or a tile

    Args:
        cog_href (str): The HREF pointing to the associated asset COG. The COG should
        be created in advance using `cog.create_cog`

    Returns:
        Item: STAC Item object
    """
    properties = {
        "title": TITLE,
        "seabed-2030:institution": INSTITUTION,
        "seabed-2030:source": SOURCE,
        "seabed-2030:history": HISTORY,
        "seabed-2030:comment": COMMENT,
    }

    try:
        item_year = re.findall(r"\d{4}", properties["title"])[0]
    except IndexError:
        raise ValueError(
            "Unable to obtain year from the dataset title attribute")

    item_datetime = datetime(int(item_year), 1, 1)

    cog_id = os.path.basename(cog_href)[:-4]

    signed_cog_href = cog_href_modifier(cog_href) if cog_href_modifier else cog_href

    with rasterio.open(signed_cog_href) as dataset:
        cog_bbox = list(dataset.bounds)
        cog_transform = list(dataset.transform)
        cog_shape = [dataset.height, dataset.width]

    x_min, y_min, x_max, y_max = cog_bbox
    item_geom = {
        "type":
        "Polygon",
        "coordinates": [[
            [x_min, y_min],
            [x_min, y_max],
            [x_max, y_max],
            [x_max, y_min],
            [x_min, y_min],
        ]],
    }

    item = Item(
        id=f"{SEABED_2030_ID}-{cog_id}",
        properties=properties,
        geometry=item_geom,
        bbox=cog_bbox,
        datetime=item_datetime,
        stac_extensions=[],
    )

    proj_attrs = ProjectionExtension.ext(item, add_if_missing=True)
    proj_attrs.epsg = SEABED_EPSG
    proj_attrs.bbox = list(cog_bbox)
    proj_attrs.shape = list(cog_shape)
    proj_attrs.transform = list(cog_transform)

    # Add the COG asset
    cog_asset = Asset(
        href=cog_href,
        media_type=MediaType.COG,
        roles=["data"],
        title="Seabed 2030 elevation",
    )
    item.add_asset("elevation", cog_asset)

    # File Extension
    cog_asset_file = FileExtension.ext(cog_asset, add_if_missing=True)
    with fsspec.open(cog_href) as file:
        size = file.size
        if size is not None:
            cog_asset_file.size = size

    # Raster Extension
    cog_asset_raster = RasterExtension.ext(cog_asset, add_if_missing=True)
    cog_asset_raster.bands = [
        RasterBand.create(
            nodata=-32767,
            unit="masl",
            sampling=Sampling.POINT,
            data_type=DataType.INT16,
            spatial_resolution=15 / 3600.0,
        )
    ]

    # Projection Extension
    cog_asset_projection = ProjectionExtension.ext(cog_asset,
                                                   add_if_missing=True)
    cog_asset_projection.epsg = SEABED_EPSG
    cog_asset_projection.bbox = cog_bbox
    cog_asset_projection.transform = list(cog_transform)
    cog_asset_projection.shape = list(cog_shape)

    return item
