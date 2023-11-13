from __future__ import print_function
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def download_logfile(sheetname="ProtoDUNE-HD_LogFile"):
    # try:
    # Set the OAuth scope and ID token audience
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    audience = 'https://www.googleapis.com/oauth2/v4/token'

    # Load credentials from the downloaded client secret file "/Users/jcapo/cernbox/DUNE-IFIC/Software/hd-tms/keys/keys.json"
    creds = ServiceAccountCredentials.from_json_keyfile_name('keys/keys.json',
                                                            scope)

    # Connect to Google Sheets API
    client = gspread.authorize(creds)

    # Open the Google Spreadsheet using the sheet name or URL
    spreadsheet = client.open('Calibration-LogFile')

    dfs = {}
    for worksheet in spreadsheet.worksheets():
        data = worksheet.get_all_values()
        df = pd.DataFrame(data[1:], columns=data[0])
        dfs[worksheet.title] = df
    worksheet = dfs[sheetname]
    return worksheet
    # except:
    #     print("No internet connection -> Downloading local LogFile")
    #     worksheet = pd.read_csv("../keys/Calibration-LogFile - DUNE-HD_LogFile.csv", header=0, dtype="str")
    #     return worksheet

def select_files(log_file, kwargs):
    selection = log_file.copy()
    print(selection)
    for i, j in kwargs.items():
        selection = selection.loc[(selection[i]==j)]
    return selection