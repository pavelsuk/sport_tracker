import logging
import logging.config
import pathlib
import json
import os


class Application():

    def __init__(self):
        """The most simple init that does initiate all internal values to None
        """
        self._logger = None
        self._active__config = None

    def init_logging(
            self,
            loggingConfigFileName: str = None,
            loggingConfigSection: str = "dbg"):
        """It initiates the application with logger

        Args:
            loggingConfigFile (str):
                full path to logging config file.
                If None, it uses current dir + 'config/logging.conf'
            loggingConfigSection (str):
                Section from the logging.conf that will be used for logging.
                If not set, the dbg will be used
        """
        if self._logger is None:
            if loggingConfigFileName is None:
                current_dir = pathlib.Path(__file__).parent
                loggingConfigFileName = current_dir.joinpath('config/logging.conf')
            logging.config.fileConfig(loggingConfigFileName)
            logger = logging.getLogger(loggingConfigSection)
            self._logger = logger
            self._logger.debug('Application.initLogging - logger created')

    @property
    def logger(self):
        return self._logger

    def read_config(self,
                    config_group: str = None,
                    config_file: str = 'config/private.configdef.json'):
        """
        Read following values from config_file (JSON) from section config_group
        Example of config_file content (config_group is test):
            "test": {
                "section1": {
               "param1": "value1"
        },
                
        Arguments:
            config_group {str}:
                name of main group that contains the configuration.
                If it's None, it looks for "active_config" key in that config file
            config_file {str}:
                relative path to config file
                If None, it uses current dir + 'config/private.configdef.json'
        """
        current_dir = pathlib.Path(__file__).parent

        with open(current_dir.joinpath(config_file), 'r') as cfg_file:
            cfg_values = json.load(cfg_file)
            if (not config_group):
                config_group = cfg_values['active_config']
            self._logger.debug('config_group= {}'.format(config_group))
            self._active__config = cfg_values[config_group]
            self._logger.debug('cfg_values= {}'.format(self._active__config))

    @property
    def config(self):
        return self._active__config


if __name__ == "__main__":
    app = Application()
