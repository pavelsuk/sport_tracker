# import logging
import pytest
import unittest

from app import Application


class Test_Application(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.app = Application()
        self.init_logging()

    def tearDown(self) -> None:
        super().tearDown()

    @pytest.mark.long
    def test__init__(self) -> None:
        self.assertIsNotNone(self.app)
        self.assertIsInstance(self.app, Application)

    def init_logging(self) -> None:
        with pytest.raises(AttributeError, match="'NoneType'"):
            self.app.logger.error('This has to throw an Exception, since the logger is not set yet')
        self.app.init_logging()

    @pytest.mark.long
    def test_init_logging_long(self) -> None:
        self.app.logger.info('Logger initiated with default values')
        self.app.logger.setLevel("CRITICAL")
        self.app.logger.info('This should not be logged')
        self.app.logger.critical('This is just a test of CRITICAL log, it should be visible in the log')
        self.app.logger.setLevel("INFO")
        self.app.logger.info('This is just a test of INFO log, it should be visible in the log')
        
    def test_read_config(self) -> None:
        self.app.read_config('test')


if __name__ == "__main__":
    unittest.main()
