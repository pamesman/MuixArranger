from google.oauth2.service_account import Credentials
import gspread


scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]

creds = Credentials.from_service_account_file("../GUI/credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "1k9W_o-bCnOd113so2OqvDfQQPLZiUnD2P29Cnni6yXs"
sheet = client.open_by_key(sheet_id)