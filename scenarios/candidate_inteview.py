from services.llm_service import LLMService
from services.crm_service import CRMService

class CandidateInterviewHandler:
    def __init__(self, user_email):
        self.llm_service = LLMService("candidate_interviewing")
        self.user_email = user_email
    
    def handle_request(self, user_input):
        if not user_input:
            return "I didn't catch that. Could you please repeat your answer?"
        
        ai_response = self.llm_service.get_response(user_input)
        
        CRMService.track_customer(
            "Candidate", 
            self.user_email, 
            f"Q: {user_input}, A: {ai_response}", 
            "candidate_interviewing"
        )
        
        return ai_response