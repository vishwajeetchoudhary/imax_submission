from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2 import service_account
from config.settings import SERVICE_ACCOUNT_FILE, SCOPES, CALENDAR_ID, TIMEZONE

class CalendarService:
    def __init__(self):
        try:
            credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES
            )
            self.calendar_service = build("calendar", "v3", credentials=credentials)
            print("Calendar service initialized successfully")
        except Exception as e:
            print(f"Error initializing calendar service: {e}")
            raise
    
    def schedule_demo(self, user_email, date_time=None, duration_hours=1):
        try:
            if not date_time:
                tomorrow = datetime.now() + timedelta(days=1)
                date_time = tomorrow.replace(hour=15, minute=0, second=0).isoformat()
            
            start_dt = datetime.fromisoformat(date_time.replace('Z', '+00:00').replace('T', ' '))
            end_dt = start_dt + timedelta(hours=duration_hours)
            
            event = {
                'summary': 'AI Demo Session',
                'description': 'Demo session for our ERP system product.',
                'start': {'dateTime': start_dt.isoformat(), 'timeZone': TIMEZONE},
                'end': {'dateTime': end_dt.isoformat(), 'timeZone': TIMEZONE},
                'attendees': [{'email': user_email}],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 30},
                    ],
                },
            }
            
            event = self.calendar_service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
            return f"Demo scheduled successfully! Details: {event.get('htmlLink')}"
        except Exception as e:
            print(f"Error scheduling demo: {e}")
            return f"Failed to schedule demo: {str(e)}"