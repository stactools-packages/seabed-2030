import stactools.core
from stactools.cli import Registry
from stactools.seabed_2030 import commands
from stactools.seabed_2030.stac import create_collection, create_item

__all__ = ['create_collection', 'create_item']

stactools.core.use_fsspec()


def register_plugin(registry: Registry) -> None:
    registry.register_subcommand(commands.create_seabed2030_command)


__version__ = "0.1.0"
