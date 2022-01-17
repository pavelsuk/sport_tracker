# import logging
# import logging.config
# import pathlib
import pytest
import unittest

from activities import Activities


class Test_Activities(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    @pytest.mark.long
    def test__init__(self) -> None:
        activities = Activities()
        self.assertIsNotNone(activities)
        self.assertIsInstance(activities, Activities)


if __name__ == "__main__":
    unittest.main()
