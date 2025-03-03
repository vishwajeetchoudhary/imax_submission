from services.llm_service import LLMService
from services.calendar_service import CalendarService
from services.crm_service import CRMService
from services.calendar_service import CalendarService

class DemoSchedulingHandler:
    def __init__(self,user_email):
        self.llm_service = LLMService("demo_scheduling")
        self.calendar_service = CalendarService()
        self.user_email = user_email
    
    def handle_request(self, user_input):
        if not user_input:
            return "I didn't catch that. Could you please repeat?"
        
        ai_response = self.llm_service.get_response(user_input)

        if "Scheduling demo" in ai_response:
            event_link = self.calendar_service.schedule_demo(self.user_email)
            print(f"Event link: {event_link}")
            
        
        return ai_response