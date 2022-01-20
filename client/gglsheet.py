import datetime
import json
# import logging
# import logging.config
import pathlib

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from typing import List

from app import Application


class GGlSheet(object):
    """
    It processes data from the list of activities
    and saves it to Google Sheet
    
    Methods:
        process_activities TODO
    """

    def __init__(self, app: Application) -> None:
        super().__init__()
        self.app = app
        self.app.logger.debug('GGlSheet.__init__')
        self.read_config()

        current_dir = pathlib.Path(__file__).parent
        self._value_input_option = 'USER_ENTERED'

        # Initialize Google Sheets

        # If modifying these scopes, delete the file token.json.
        # SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly' 
        SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

        store = file.Storage(current_dir.joinpath('config/private.token.json'))
        creds = store.get()
        if not creds or creds.invalid:
            self.app.logger.debug('GGlSheet invalid creds')
            flow = client.flow_from_clientsecrets(current_dir.joinpath('config/private.credentials.json'), SCOPES)
            creds = tools.run_flow(flow, store)
        self.app.logger.debug('GGlSheet before build')
        self.service = build('sheets', 'v4', http=creds.authorize(Http()), cache_discovery=False)

    def read_config(self):
        """
        Read following values from config_file (JSON) from section config_group
        Example of config_file content (config_group is test):
            "test": {
                "gglsheet": {
                "sheet_id" : "<put_your_sheet_id_here>",
                "event_sheet_name" : "<your_sheet_name_for_events>",
                "ip_info_sheet_name" : "IP Info",
                "ip_info_col_ip" : "A:A"

                },
                
        Arguments:
            config_group {str} -- name of main group that contains sheet_id, event_sheet_name.
                                  If it's None, it looks for "active_config" key in that config file
            config_path {str} -- relative path to config file
        """
        # current_dir = pathlib.Path(__file__).parent

        cfg_group_map = self.app.config['gglsheet']
        self.app.logger.debug('cfg_group_map= {}'.format(cfg_group_map))
        self._spreadsheet_id = cfg_group_map['sheet_id']
        self._event_sheet_name = cfg_group_map['activities_sheet_name']
        self._event_col_time = self._event_sheet_name + '!' + cfg_group_map['activities_col_time']

    def append_values(self, _values, _range_name):
        service = self.service
        self.app.logger.debug('GGlSheet.append_values SpreadsheetID: {}, RangeName: {}'.format(
            self._spreadsheet_id, _range_name))
        # [START sheets_append_values]
        values = [
            [
                # Cell values ...
            ],
            # Additional rows ...
        ]
        # [START_EXCLUDE silent]
        values = _values
        # [END_EXCLUDE]
        body = {'values': values}
        result = service.spreadsheets().values().append(
            spreadsheetId=self._spreadsheet_id, range=_range_name, valueInputOption=self._value_input_option,
            body=body).execute()
        self.app.logger.debug('{0} cells appended.'.format(result.get('updates').get('updatedCells')))
        # [END sheets_append_values]
        return result

    def read_values(self, _range_name, skip_header: bool = True, majorDimension='ROWS'):
        service = self.service
        self.app.logger.debug('GGlSheet.read_values SpreadsheetID: {}, RangeName: {}'.format(
            self._spreadsheet_id, _range_name))

        result = service.spreadsheets().values().get(
            spreadsheetId=self._spreadsheet_id, majorDimension=majorDimension, range=_range_name).execute()

        # TODO if skip_header and majorDimension == 'COLUMNS'
        # and there are more columns in the range, I must
        # return all columns and remove all headers
        retVal = result['values'][1:] if skip_header and majorDimension == 'ROWS'\
            else result['values'][0][1:] if skip_header \
            else result['values'] if (not skip_header) and majorDimension == 'ROWS' \
            else result['values'][0]

        self.app.logger.debug('GGlSheet.read_values result \n {0}'.format(retVal))

        return retVal

    def process_activities(self, act_list: List) -> int:
        """
        Processes activity list:
            - Saves data to table of events

        Arguments:
            act_list {List} -- List of activities with following structure
        
        Returns:
            int -- number of rows updated
        """
        return self.process_new_activities(
            act_list, datetime.datetime.strptime('01.01.2000', '%d.%m.%Y'))

    def process_new_activities(
            self,
            act_list: List,
            newer_than: datetime = None) -> int:

        """
        Processes event list:
            - Saves new data to table of events

        Arguments:
        Processes activity list:
            - Saves data to table of events

        Arguments:
            act_list {List} -- List of activities with following structure
            newer_than(datetime) -- it will import all activities that are newer than this datetime
                                    if it is None, it reads the latest timestamp from database
        Returns:
            int -- number of rows updated

        """

        self.app.logger.debug('process_new_activities - START, act_list: {}'.format(act_list))
        retVal = 0
        if (not act_list):
            return retVal

        if not (newer_than):
            newer_than = self.get_latest_activity_time()

        rows_base = []
        for row in act_list:
            if(datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S') > newer_than):
                rows_base.append(row)

            """
            if datetime.datetime.strptime(ev['EventTime'], '%Y-%m-%d %H:%M:%S') > newer_than:
                values.append([ev['EventTime'], ev['IPAddr'], ev_src, ev_type, ev_info])
            """
        
        self.app.logger.debug('process_new_activities - values: {}'.format(rows_base))
        
        if rows_base:
            retVal = self.append_values(rows_base, self._event_sheet_name)['updates']['updatedRows']
        
        self.app.logger.info('process_new_events - {} new events'.format(retVal))
        return retVal

    def get_latest_activity_time(self) -> datetime:
        """
        Returns the latest event time from sheet defined in configdef.json
            "event_sheet_name" : "<name of the sheet with IP addresses",
            "event_col_time" : "<range - typically column>"
    
        Returns:
            datetime of the latest event

        """
        all_rows = self.read_values(self._event_col_time, skip_header=True, majorDimension='COLUMNS')
        retVal = datetime.datetime.strptime('01.01.2000', '%d.%m.%Y')
        for row in all_rows:
            row_dt = datetime.datetime.strptime(row, '%Y-%m-%d %H:%M:%S')
            if retVal < row_dt:
                retVal = row_dt
        self.app.logger.debug('get_latest_eventtime : {}'.format(retVal))
        return retVal


if __name__ == "__main__":
    pass
