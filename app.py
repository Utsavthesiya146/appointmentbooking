# import streamlit as st
# import requests

# st.title("Appointment Booking Assistant")

# user_input = st.text_input("How can I assist you today?")

# if st.button("Send"):
#     # Call the FastAPI backend to process the user input
#     response = requests.post("AIzaSyCVRc9vDiGBj1T391RF6ZmxCHFFbuJcP8w", json={"input": user_input})
#     st.write(response.json())
   


# app.py
import streamlit as st
from datetime import datetime, timedelta
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

# Google Calendar Setup
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'service_account-file.json'  # Create this file as shown below
calendar_id = "9d23676d1e15e9140e9cc944f3ff3355740f76401fa468835d8107fd4a96817d@group.calendar.google.com"  # Use "primary" for your main calendar

# Sample service account JSON - REPLACE WITH YOUR ACTUAL FILE
SERVICE_ACCOUNT_JSON ="service-account-file.json"

# Helper Functions
def get_calendar_service():
    """Authenticate with Google Calendar using service account"""
    credentials = service_account.Credentials.from_service_account_info(
        json.loads(SERVICE_ACCOUNT_JSON), 
        scopes=SCOPES
    )
    return build('calendar', 'v3', credentials=credentials)

def check_availability(service, start_time, end_time):
    """Check if time slot is available"""
    events_result = service.events().list(
        calendarId="9d23676d1e15e9140e9cc944f3ff3355740f76401fa468835d8107fd4a96817d@group.calendar.google.com" ,
        timeMin=start_time,
        timeMax=end_time,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return not bool(events_result.get('items', []))

def create_event(service, event_details):
    """Create a new calendar event"""
    event = {
        'summary': event_details['summary'],
        'description': event_details.get('description', ''),
        'start': {
            'dateTime': event_details['start'],
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': event_details['end'],
            'timeZone': 'America/New_York',
        },
    }
    
    return service.events().insert(calendarId="9d23676d1e15e9140e9cc944f3ff3355740f76401fa468835d8107fd4a96817d@group.calendar.google.com ", body=event).execute()

# Streamlit UI
st.set_page_config(page_title="Calendar Booking Assistant", layout="wide")

# Custom CSS for chat interface
st.markdown("""
<style>
.chat-box {
    border: 1px solid #e1e4e8;
    border-radius: 8px;
    padding: 16px;
    margin: 8px 0;
    background-color: #f9f9f9;
}
.bot-message {
    padding: 12px;
    border-radius: 8px 8px 8px 0;
    background-color: #f0f2f6;
    margin-bottom: 8px;
}
.user-message {
    padding: 12px;
    border-radius: 8px 8px 0 8px;
    background-color: #e3f2fd;
    margin-bottom: 8px;
    text-align: right;
}
</style>
""", unsafe_allow_html=True)

# Initialize chat session
if 'messages' not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hello! I'm your appointment booking assistant. How can I help you today?"
    }]

# Display chat messages
for message in st.session_state.messages:
    st.markdown(
        f'<div class="{message["role"] + "-message"}">{message["content"]}</div>',
        unsafe_allow_html=True
    )

# User input
if user_input := st.chat_input("Type your message..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    st.markdown(
        f'<div class="user-message">{user_input}</div>',
        unsafe_allow_html=True
    )
    
    # Initialize response
    response = ""
    
    try:
        service = get_calendar_service()
        
        # Simple NLP logic - in a real app you'd use LangChain
        if "book" in user_input.lower() or "appointment" in user_input.lower():
            # Simplified - you would parse the actual datetime in a real app
            suggested_time = (datetime.now(pytz.timezone("America/New_York")) + 
                            timedelta(hours=1)).isoformat()
            end_time = (datetime.now(pytz.timezone("America/New_York")) + 
                       timedelta(hours=2)).isoformat()
            
            if check_availability(service, suggested_time, end_time):
                response = f"I can book you for {suggested_time.split('T')[0]} at {suggested_time.split('T')[1][:5]}. Does this work for you?"
                # In a real app you'd store this state to confirm
            else:
                response = "I don't see availability at that time. Please try another time."
        else:
            response = "I can help you book appointments on your calendar. Please tell me what date and time works for you."
            
    except Exception as e:
        response = f"Sorry, I encountered an error: {str(e)}"
    
    # Add assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Display assistant response
    st.markdown(
        f'<div class="bot-message">{response}</div>',
        unsafe_allow_html=True
    )

    # Force rerun to display new messages
    st.rerun()
