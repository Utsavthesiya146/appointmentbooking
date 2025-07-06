from fastapi import FastAPI, HTTPException
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import json

app = FastAPI()

# Load the service account credentials
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'D:\appointmentbooking\backend\service-account-file.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)

@app.get("/check_availability")
async def check_availability(start_time: str, end_time: str):
    # Check availability logic
    pass

@app.post("/book_appointment")
async def book_appointment(event_details: dict):
    # Booking logic
    pass
