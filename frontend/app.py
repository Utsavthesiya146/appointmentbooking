# frontend/app.py
import streamlit as st
from datetime import datetime, timedelta
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Calendar Config
SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "../backend/service_account-file.json"
CALENDAR_ID = "primary"  # Replace with actual calendar ID if needed

def get_calendar_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build("calendar", "v3", credentials=credentials)

def check_availability(service, start_time, end_time):
    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_time,
        timeMax=end_time,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return not bool(events_result.get('items', []))

def create_event(service, summary, start_time, end_time):
    event = {
        'summary': summary,
        'start': {'dateTime': start_time, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time, 'timeZone': 'Asia/Kolkata'},
    }
    return service.events().insert(calendarId=CALENDAR_ID, body=event).execute()

# Streamlit Chat UI
st.set_page_config(page_title="Calendar Booking Assistant", layout="centered")
st.title("📅 Calendar Booking Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I can help you book an appointment. Tell me your preferred time."}]

# Display message history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle user input
if user_input := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            service = get_calendar_service()

            # Suggest slot 1 hour from now for 1 hour
            now = datetime.now(pytz.timezone("Asia/Kolkata"))
            start_time = now + timedelta(hours=1)
            end_time = start_time + timedelta(hours=1)
            start_iso = start_time.isoformat()
            end_iso = end_time.isoformat()

            if check_availability(service, start_iso, end_iso):
                msg = f"I found a free slot at {start_time.strftime('%I:%M %p')} on {start_time.strftime('%d %b %Y')}. Should I book it?"
            else:
                msg = "That time slot is already booked. Please suggest another time."

        except Exception as e:
            msg = f"⚠️ Sorry, something went wrong: `{e}`"

        st.markdown(msg)
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.rerun()
