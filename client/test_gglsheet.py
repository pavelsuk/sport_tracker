# import logging
# import logging.config
# import pathlib
import pytest
import unittest

from app import Application
from gglsheet import GGlSheet


class Test_GGlSheet(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.app = Application()
        self.app.init_logging()
        self.app.read_config(config_group='test')
        ggl_sheet = GGlSheet(self.app)
        self.assertIsNotNone(ggl_sheet)
        self.assertIsInstance(ggl_sheet, GGlSheet)
        self.ggl_sheet = ggl_sheet

    def tearDown(self) -> None:
        super().tearDown()

    def test_GGlSheet_class(self):
        self.assertIsNotNone(self.ggl_sheet)
        self.assertIsInstance(self.ggl_sheet, GGlSheet)

    def test_get_latest_activity_time(self) -> None:
        tm = self.ggl_sheet.get_latest_activity_time()
        self.app.logger.debug(f'test_get_latest_activity_time: {tm}')


if __name__ == "__main__":
    unittest.main()
