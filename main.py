# from fastapi import FastAPI, HTTPException
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from datetime import datetime, timedelta
# import json

# app = FastAPI()

# # Load the service account credentials
# SCOPES = ['https://www.googleapis.com/auth/calendar']
# SERVICE_ACCOUNT_FILE = 'D:\appointmentbooking\backend\service-account-file.json'

# credentials = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# service = build('calendar', 'v3', credentials=credentials)

# @app.get("/check_availability")
# async def check_availability(start_time: str, end_time: str):
#     # Check availability logic
#     pass

# @app.post("/book_appointment")
# async def book_appointment(event_details: dict):
#     # Booking logic
#     pass










# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
import os

app = FastAPI()

# Google Calendar Config
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = "service_account-file.json"
CALENDAR_ID = "primary"

# Google API Setup
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)

# Data models
class Slot(BaseModel):
    start_time: datetime
    end_time: datetime

class Event(BaseModel):
    summary: str
    start_time: datetime
    end_time: datetime

@app.post("/check_availability")
def check_availability(slot: Slot):
    try:
        events_result = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=slot.start_time.isoformat(),
            timeMax=slot.end_time.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        return {"available": not bool(events_result.get('items', []))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/book_appointment")
def book_appointment(event: Event):
    try:
        event_body = {
            'summary': event.summary,
            'start': {'dateTime': event.start_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
            'end': {'dateTime': event.end_time.isoformat(), 'timeZone': 'Asia/Kolkata'}
        }
        service.events().insert(calendarId=CALENDAR_ID, body=event_body).execute()
        return {"status": "success", "message": "Appointment booked successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
