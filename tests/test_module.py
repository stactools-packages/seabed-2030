import unittest

import stactools.seabed_2030


class TestModule(unittest.TestCase):
    def test_version(self):
        self.assertIsNotNone(stactools.seabed_2030.__version__)
