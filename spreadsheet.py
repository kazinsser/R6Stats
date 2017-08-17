import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheet:
    __sheet = 0;

    def __init__(self):
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('GDrive.json', scope)
        client = gspread.authorize(creds)
        self.__sheet = client.open('R6Stats').sheet1

    def getSheet(self):
        return self.__sheet
