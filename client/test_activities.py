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
    def test_Init(self) -> None:
        self.activities = Activities()
        self.assertIsNotNone(self.activities)
        self.assertIsInstance(self.activities, Activities)


if __name__ == "__main__":
    unittest.main()