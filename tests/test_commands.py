import os.path
from tempfile import TemporaryDirectory

from tests import test_data

import pystac
from stactools.seabed_2030.commands import create_seabed2030_command
from stactools.testing import CliTestCase


def get_test_path(ext):
    test_path = test_data.get_path("data-files")
    path = [
        os.path.join(test_path, d) for d in os.listdir(test_path)
        if d.lower().endswith(f".{ext}")
    ][0]
    return path


class CommandsTest(CliTestCase):
    def create_subcommand_functions(self):
        return [create_seabed2030_command]

    def test_create_cog(self):
        path = get_test_path("nc")

        with TemporaryDirectory() as tmp_dir:
            cog_path = os.path.join(tmp_dir,
                                    os.path.basename(path)[:-3] + "_cog.tif")
            result = self.run_command(
                ["seabed2030", "create-cog", path, cog_path])

            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))

            cogs = [p for p in os.listdir(tmp_dir) if p.endswith("_cog.tif")]
            self.assertEqual(len(cogs), 1)

    def test_create_collection(self):
        with TemporaryDirectory() as tmp_dir:
            destination = os.path.join(tmp_dir, "collection.json")

            result = self.run_command(
                ["seabed2030", "create-collection", destination])

            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            collection = pystac.read_file(destination)
            self.assertEqual(collection.id, "seabed-2030")

            collection.validate()

    def test_create_item(self):
        path = get_test_path("tif")

        with TemporaryDirectory() as tmp_dir:
            destination = os.path.join(tmp_dir, "item.json")
            result = self.run_command(
                ["seabed2030", "create-item", path, destination])
            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            item = pystac.read_file(destination)
            self.assertEqual(item.id, "seabed-2030-GEBCO_2020_5_7_01_01")

            item.validate()
