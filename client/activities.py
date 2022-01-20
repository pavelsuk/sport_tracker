import pathlib
import csv
import os

from app import Application
from gglsheet import GGlSheet

class Activities(object):
    '''Data holder for activities.
    The data can be read from CSV, stored directly to google sheet or to database through API
    '''

    def __init__(self, app: Application) -> None:
        super().__init__()
        self.app = app
        self.app.logger.debug('Activities.__init__')
        self._csv_fname = None
        self.read_config()

    def read_config(self):
        config_group = self.app.config['activities']
        csv_fName = config_group["csv_fname"]

        if(csv_fName):
            current_dir = pathlib.Path(__file__).parent
            self._csv_fname = os.path.join(current_dir, csv_fName)

        self.app.logger.debug('self._csv_fname= {}'.format(self._csv_fname))
        
        csv_fName_update = config_group["csv_fname_update"]
        if(csv_fName_update):
            current_dir = pathlib.Path(__file__).parent
            self._csv_fName_update = os.path.join(current_dir, csv_fName_update)
        self.app.logger.debug('self._csv_fName_update= {}'.format(self._csv_fName_update))
        
        self._required_fields = config_group["required_fields"]
        self.app.logger.debug('self._required_fields= {}'.format(self._required_fields))
        
    def filter_fields(self, listDictIn, asList: bool = False, required_fields=None):
        outRows = []
        for rowIn in listDictIn:
            self.app.logger.debug(f'filter_fields: rowIn {rowIn}')
            if (asList):
                outRow = []
            else:
                outRow = {}
            if(required_fields is None):
                required_fields = self._required_fields
            for required_field in required_fields:
                if(asList):
                    outRow.append(rowIn.get(required_field))
                else:
                    outRow[required_field] = rowIn.get(required_field)
            outRows.append(outRow)
            self.app.logger.debug(f'filter_fields: rowOut {outRow}')
            
        self.app.logger.debug('----     all rows ----------')
        self.app.logger.debug(outRows)
        return outRows

    def order_by(self, rows: list, key_column=None, reverse=False) -> list:
        if key_column is None:
            key_column = "Date"

        return sorted(rows, key=lambda row: row[key_column], reverse=reverse)

    def merge_2_lists(self, rows_base: list, rows_updates: list) -> list:
        """
            It merges 2 lists together, based on "Date| field.
            All rows from base are imported + the ones that are newer than the newest from base

        Args:
            rows_base (list): Original list of rows
            rows_updates (list): Updates

        Returns:
            list: merged list
        """
        if(rows_base is None):
            return rows_updates
        if(len(rows_base) == 0):
            return rows_updates

        last_date = self.order_by(rows_base, "Date", reverse=True)[0]["Date"]
        self.app.logger.debug(f'last_date: {last_date}')

        for row in rows_updates:
            if(row["Date"] > last_date):
                rows_base.append(row)

        self.app.logger.debug(f'merged list: {rows_base}')
        return rows_base

    def read_from_CSV(self, csv_fname=None, asList: bool = False) -> list:
        if csv_fname is None:
            csv_fname = self._csv_fname
            
        outRows = []
        with open(csv_fname, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            outRows = self.filter_fields(reader, asList)

        self.app.logger.debug(f'read_from_CSV: {outRows}')
        return outRows

    def update(self) -> list:
        self.app.logger.debug('update(self) self._csv_fname= {}'.format(self._csv_fname))
        self.app.logger.debug('update(self) self._csv_fName_update= {}'.format(self._csv_fName_update))
        base_list = self.read_from_CSV(self._csv_fname)
        update_list = self.read_from_CSV(self._csv_fName_update)
        new_list = self.merge_2_lists(base_list, update_list)
        self.app.logger.debug(f'new_list: {new_list}')

    def updateGglSheet(self):
        self.app.logger.debug('updateGglSheet(self) self._csv_fName_update= {}'.format(self._csv_fName_update))
        act_list = self.read_from_CSV(self._csv_fName_update, True)
        gglSheet = GGlSheet(self.app)
        updatedRowNumber = gglSheet.process_new_activities(act_list)
        self.app.logger.debug(f'updateGglSheet(self) updatedRowNumber: {updatedRowNumber}')


if __name__ == "__main__":
    activities = Activities()
