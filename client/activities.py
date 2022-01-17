import logging
import logging.config
import pathlib
import json
import os

from app import Application


class Activities(object):
    '''Data holder for activities.
    The data can be read from CSV, stored directly to google sheet or to database through API
    '''

    def __init__(self, app: Application) -> None:
        super().__init__()
        self.app = app
        self.app.logger.debug('Activities.__init__')
        self.read_config()

    def read_config(self):
        config_group = self.app.config['csv']
        csv_fName = config_group["filename"]
        current_dir = pathlib.Path(__file__).parent
        self._csv_fname = os.path.join(current_dir, csv_fName)
        self.app.logger.debug('self._csv_fname= {}'.format(self._csv_fname))


if __name__ == "__main__":
    activities = Activities()
