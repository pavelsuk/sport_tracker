import logging
import logging.config
import pathlib
import json
import os


class Activities(object):
    '''Data holder for activities.
    The data can be read from CSV, stored directly to google sheet or to database through API
    '''

    def __init__(self,
                 config_group: str = None,
                 config_file: str = 'config/private.configdef.json',
                 logger=None,
                 csv_fName: str = None):
        if logger is None:
            current_dir = pathlib.Path(__file__).parent
            logfile = current_dir.joinpath('config/logging.conf')
            logging.config.fileConfig(logfile)
            logger = logging.getLogger('dbg')
        self.logger = logger
        self.logger.debug('Activities.__init__')
        self.read_config(config_group, config_file, csv_fName)

    # TODO: read_config should be global or config itself should be global
    def read_config(self,
                    config_group: str = None,
                    config_file: str = 'config/private.configdef.json',
                    csv_fName: str = None):
        """
        Read following values from config_file (JSON) from section config_group
        Example of config_file content (config_group is test):
            "test": {
                "csv": {
               "filename": "files/test_Activities.csv"
        },
                
        Arguments:
            config_group {str} -- name of main group that contains the configuration.
                                  If it's None, it looks for "active_config" key in that config file
            config_file {str} -- relative path to config file
        """
        current_dir = pathlib.Path(__file__).parent

        with open(current_dir.joinpath(config_file), 'r') as cfg_file:
            cfg_values = json.load(cfg_file)
            if (not config_group):
                config_group = cfg_values['active_config']
            self.config = cfg_values[config_group]['csv']
            if (not csv_fName):
                csv_fName = self.config["filename"]
            self.logger.debug('cfg_values= {}'.format(cfg_values))

            self._csv_fname = os.path.join(current_dir, csv_fName)
            self.logger.debug('self._csv_fname= {}'.format(self._csv_fname))


if __name__ == "__main__":
    activities = Activities()
