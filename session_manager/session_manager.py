from scenarios.candidate_inteview import CandidateInterviewHandler
from scenarios.demo_scheduling import DemoSchedulingHandler
from scenarios.payment_followup import PaymentFollowupHandler

class SessionManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance._initialized = False  # Ensure initialization happens only once
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.handler = None
            print("SessionManager initialized")
            self._initialized = True  # Mark as initialized
            self.email = None
            self.scenario = None

    def update_handler(self, scenario, user_email):
        if scenario == "1":
            self.handler = DemoSchedulingHandler(user_email)
        elif scenario == "2":
            self.handler = CandidateInterviewHandler(user_email)
        elif scenario == "3":
            self.handler = PaymentFollowupHandler(user_email)
        else:
            self.handler = None
        self.email = user_email
        self.scenario = scenario
        print(f"Handler updated to {scenario} with email {user_email}")

    def get_handler(self):
        return self.handler
    
    def get_scenario(self):
        return self.scenario
