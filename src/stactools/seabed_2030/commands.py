import click
import logging

from stactools.seabed_2030 import stac
from stactools.seabed_2030 import cog
from stactools.seabed_2030.constants import THUMBNAIL

logger = logging.getLogger(__name__)


def create_seabed2030_command(cli: click.Group) -> click.Command:
    """Creates the stactools-seabed-2030 command line utility."""
    @cli.group(
        "seabed2030",
        short_help=("Commands for working with stactools-seabed-2030"),
    )
    def seabed2030() -> None:
        pass

    @seabed2030.command(
        "create-cog",
        short_help="Creates a COG from a GECBO netcdf file",
    )
    @click.argument("source")
    @click.argument("destination")
    @click.option(
        "-n",
        "--name",
        help="The name of the Elevation dataset",
        default="elevation",
    )
    @click.option(
        "-n",
        "--retile",
        help="Directory to retile COGs into",
        default=None,
    )
    def create_cog_command(source: str, destination: str, name: str,
                           retile: str) -> None:
        """Creates a STAC Collection

        Args:
            source (str): An HREF for the GECBO netcdf file
            destination (str): An HREF for the Collection JSON
            name (str, optional): Elevation dataset name in the GECBO file.
            retile (str, optional): Directory to use for retiling
            Defaults to 'elevation'.
        """
        cog.create_cog(source, destination, name, retile)

    @seabed2030.command(
        "create-collection",
        short_help="Creates a STAC collection",
    )
    @click.argument("destination")
    @click.option(
        "-t",
        "--thumbnail",
        help="HREF to a thumbnail for the collection",
        default=THUMBNAIL,
    )
    def create_collection_command(destination: str, thumbnail: str) -> None:
        """Creates a STAC Collection

        Args:
            destination (str): An HREF for the Collection JSON
            thumbmail (str): HREF to a thumbnail for the collection
        """
        collection = stac.create_collection(thumbnail_url=thumbnail)

        collection.set_self_href(destination)

        collection.save_object()

    @seabed2030.command("create-item", short_help="Create a STAC item")
    @click.argument("cog_href")
    @click.argument("destination")
    def create_item_command(cog_href: str, destination: str) -> None:
        """Creates a STAC Item

        Args:
            destination (str): An HREF for the STAC Collection
            cog_href (str): An HREF for the associated COG asset
            thumbnail (str): An HREF for a thumbmail
        """
        item = stac.create_item(cog_href)

        item.save_object(dest_href=destination)

    return seabed2030
