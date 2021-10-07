from typing import Union
from subprocess import run

from stactools.core.utils.convert import cogify


def create_cog(
    nc_href: str,
    cog_href: str = None,
    ds_name: str = "elevation",
    retile_dir: Union[str, None] = None,
    retile_size: int = 10000,
) -> None:
    """Create a COG from a GECBO Grid netcdf file

    Args:
        nc_href (str): HREF pointing to a GECBO Grid netcdf file
        cog_href (str, optional): HREF pointing to an output COG file. Defaults to None
        ds_name (str, optional): Elevation dataset name in the GECBO file.
        retile_dir (str, optional): If retiled cogs are required an output directory
        may be provided. Defaults to None (creates a single COG).
        retile_size (int, optional): A tile size to use if a `retile_dir`
        is specified. Defaults to 10000.
        Defaults to 'elevation'.
    """
    if cog_href is None and retile_dir is None:
        raise ValueError(
            'One of either cog_href or retile_dir must be specified')

    if retile_dir is not None:
        cmd = [
            "gdal_retile.py",
            "-targetDir",
            retile_dir,
            "-ps",
            retile_size,
            retile_size,
            "-of",
            "GTiff",
            "-co",
            "TILED=YES",
            "-co",
            "BLOCKYSIZE=512",
            "-co",
            "BLOCKXSIZE=512",
            "-co",
            "COMPRESS=LZW",
            "-s_srs",
            "EPSG:4326",
            f'NETCDF:"{nc_href}":{ds_name}',
        ]
        run(cmd, check=True)

    else:
        cogify(f'NETCDF:"{nc_href}":{ds_name}', cog_href,
               ["-co", "compress=LZW"])
