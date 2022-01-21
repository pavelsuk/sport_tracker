import argparse

from activities import Activities
from app import Application


class RunCheck(object):

    PGM_VERSION = '0.1'

    def __init__(self):
        app = Application()
        app.init_logging()
        
        self.app = app
        # self.logger = app.logger
        self._slParser = None
        self._csv_fname = None

    def parse_args(self):
        retVal = True

        # construct the argument parse and parse the arguments
        ap = argparse.ArgumentParser(description='Imports sports data')
        ap.add_argument('csv', help='input file', nargs='?', default=None)
        ap.add_argument(
            "-v",
            "--verbosity",
            help="level of verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL) Default: ERROR",
            default='ERROR')
        ap.add_argument(
            "-c",
            "--configfile",
            help="Path to config file. Default: config/private.configdef.json",
            default='config/private.configdef.json')
        ap.add_argument(
            "-g", "--configgroup", help="Configuration group within config file, Default: None = Active", default=None)

        args = ap.parse_args()
        self._configfile = args.configfile
        self._configgroup = args.configgroup

        verb_choices = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        verbose_lvl = 'ERROR'
        self.app.logger.setLevel(verbose_lvl)

        if (args.verbosity):
            verbose_lvl = args.verbosity.upper()
            if (verbose_lvl in verb_choices):
                self.app.logger.setLevel(verbose_lvl)
                self.app.logger.debug('Verbosity level :{}'.format(verbose_lvl))
            else:
                print('Verbosity must be one of the following values: DEBUG, INFO, WARNING, ERROR, CRITICAL')
                retVal = False

        self._csv_fname = args.csv
        if (args.csv):
            self.app.logger.debug('csv file: {}'.format(self._csv_fname))
        else:
            self.app.logger.debug('csv file not set, default value from the config will be used')

        if (not retVal):
            ap.print_help()

        return retVal

    def parse_csv(self, csv_fname: str = None):
        if (not csv_fname):
            csv_fname = self._csv_fname

        # TODO - return parsed CSV

    def run(self):
        if (self.parse_args()):
            self.app.read_config(self._configgroup, self._configfile)

            # Let's parse the CSV file
            if(self._csv_fname):
                self.app.logger.info('Reading from {}'.format(self._csv_fname))
            else:
                self.app.logger.debug('NO CSV on command line, using config ')
            
            activities = Activities(self.app)
            activities.updateGglSheet()
            self.app.logger.info('Job finished')
                
           
if __name__ == "__main__":
    runner = RunCheck()
    runner.run()
