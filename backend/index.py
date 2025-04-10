from fastapi import FastAPI , HTTPException
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import db , credentials
from dotenv import load_dotenv
import os 

load_dotenv()

app = FastAPI()

load_dotenv()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def initialize_firebase():
    try:
        firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate("../data_ingestion/firebaseConfig.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': os.getenv("FIREBASE_DATABASE_URL")
        })

# Initialize Firebase on startup
initialize_firebase()

@app.get("/")
async def root () :
    return {"message" : "Hello World"}


@app.get("/sheets-data")
async def get_sheets_data(path: str = "sheets_data"):
    try :
        ref = db.reference(path)

        data = ref.get()

        if data is None:
            raise HTTPException(status_code=404 , detail=f"No data found in '{path}'")
        
        return data
    
    except Exception as e:
        raise HTTPException(status_code=500 , detail=f"Failed to fetch data : {str(e)} ")

