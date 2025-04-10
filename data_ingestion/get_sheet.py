import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_sheet_data(spreadsheet_id , api_key):
    
        
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/!A1:Z?alt=json&key={api_key}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        return data
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


#https://docs.google.com/spreadsheets/d/1AGEog1vA3wvdxQ-C7Wy4X4a_TkKRuvt9bXOtnXtQtSQ/edit?usp=sharing

spreadsheet_id = '1AGEog1vA3wvdxQ-C7Wy4X4a_TkKRuvt9bXOtnXtQtSQ'

api_key = os.getenv("GOOGLE_SHEETS_API_KEY")

sheet_data = get_sheet_data(spreadsheet_id , api_key)

if sheet_data:
    print(sheet_data)
else:
    print("Failed to fetch data from Google Sheets API.")
