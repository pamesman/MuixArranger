from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import gspread


scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)


def spreadsheet_connection(sheet_id):
    try:
        sheet = client.open_by_key(sheet_id)
    except:
        sheet_id = "1k9W_o-bCnOd113so2OqvDfQQPLZiUnD2P29Cnni6yXs"
        sheet = client.open_by_key(sheet_id)

    drive = build("drive", "v3", credentials=creds)
    return sheet, drive