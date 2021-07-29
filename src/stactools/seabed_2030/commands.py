import click
import logging

from stactools.seabed_2030 import stac
from stactools.seabed_2030 import cog

logger = logging.getLogger(__name__)


def create_seabed2030_command(cli):
    """Creates the stactools-seabed-2030 command line utility."""
    @cli.group(
        "seabed2030",
        short_help=("Commands for working with stactools-seabed-2030"),
    )
    def seabed2030():
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
        default='elevation',
    )
    def create_cog_command(source: str, destination: str, name: str):
        """Creates a STAC Collection

        Args:
            source (str): An HREF for the GECBO netcdf file
            destination (str): An HREF for the Collection JSON
            name (str, optional): Elevation dataset name in the GECBO file.
            Defaults to 'elevation'.
        """
        cog.create_cog(source, destination, name)

    @seabed2030.command(
        "create-collection",
        short_help="Creates a STAC collection",
    )
    @click.argument("destination")
    def create_collection_command(destination: str):
        """Creates a STAC Collection

        Args:
            destination (str): An HREF for the Collection JSON
        """
        collection = stac.create_collection()

        collection.set_self_href(destination)

        collection.save_object()

    @seabed2030.command("create-item", short_help="Create a STAC item")
    @click.argument("source")
    @click.argument("destination")
    @click.argument("cog_href")
    def create_item_command(source: str, destination: str, cog_href: str):
        """Creates a STAC Item

        Args:
            source (str): HREF of the Asset associated with the Item
            destination (str): An HREF for the STAC Collection
            cog_href (str): An HREF for the associated COG asset
        """
        item = stac.create_item(source, cog_href)

        item.save_object(dest_href=destination)

    return seabed2030
