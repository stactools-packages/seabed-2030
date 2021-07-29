from stactools.core.utils.convert import cogify


def create_cog(nc_href: str, cog_href: str, ds_name: str = "elevation"):
    """Create a COG from a GECBO Grid netcdf file

    Args:
        nc_href (str): HREF pointing to a GECBO Grid netcdf file
        cog_href (str): HREF pointing to an output COG file
        ds_name (str, optional): Elevation dataset name in the GECBO file.
        Defaults to 'elevation'.
    """
    cogify(f'NETCDF:"{nc_href}":{ds_name}', cog_href, ["-co", "compress=LZW"])
