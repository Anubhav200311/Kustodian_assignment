import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
from getSheet import get_sheet_data


# Initialize Firebase
cred = credentials.Certificate("./firebaseConfig.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': f'{os.getenv("FIREBASE_DATABASE_URL")}'
})

def upload_to_firebase(data, ref_path='sheets_data'):
    """
    Upload data to Firebase Realtime Database
    
    Args:
        data: The data to upload
        ref_path: The reference path in the database
    """
    try:
        # Get a database reference
        ref = db.reference(ref_path)
        
        if 'values' in data:
            headers = data['values'][0]
            
            # Convert rows to dictionaries
            transformed_data = []
            for row in data['values'][1:]:
                item = {}
                for i, value in enumerate(row):
                    if i < len(headers):  # Ensure we have a header for this column
                        item[headers[i]] = value
                transformed_data.append(item)
                
            # Upload the transformed data
            ref.set(transformed_data)
            print(f"Successfully uploaded {len(transformed_data)} rows to Firebase")
            return True
        else:
            # Upload the data as is
            ref.set(data)
            print("Successfully uploaded data to Firebase")
            return True
            
    except Exception as e:
        print(f"Error uploading to Firebase: {e}")
        return False

if __name__ == "__main__":
    # Get your spreadsheet data
    spreadsheet_id = "1AGEog1vA3wvdxQ-C7Wy4X4a_TkKRuvt9bXOtnXtQtSQ"
    api_key = os.getenv("GOOGLE_SHEETS_API_KEY")
    
    # Extract data from Google Sheets
    sheet_data = get_sheet_data(spreadsheet_id, api_key)
    
    if sheet_data:
        # Upload to Firebase
        upload_to_firebase(sheet_data)
    else:
        print("No data to upload")