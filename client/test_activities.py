# import logging
# import logging.config
# import pathlib
import pytest
import unittest

from app import Application
from activities import Activities


class Test_Activities(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.app = Application()
        self.app.init_logging()
        self.app.read_config(config_group='test')
        activities = Activities(self.app)
        self.assertIsNotNone(activities)
        self.assertIsInstance(activities, Activities)
        self.activities = activities

    def tearDown(self) -> None:
        super().tearDown()

    def test_activites_class(self):
        self.assertIsNotNone(self.activities)
        self.assertIsInstance(self.activities, Activities)

    def test_read_from_CSV(self):
        self.activities.read_from_CSV()

    def test_update(self):
        self.activities.update()

    def test_updateGglSheet(self):
        self.activities.updateGglSheet()
if __name__ == "__main__":
    unittest.main()
