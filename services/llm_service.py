import time
from langchain_openai import ChatOpenAI
from config.settings import OPEN_AI_KEY, LLM_MODEL
from prompts.system_prompts import SYSTEM_PROMPTS

class LLMService:
    def __init__(self,scenario):
        try:
            self.llm = ChatOpenAI(model_name=LLM_MODEL, api_key=OPEN_AI_KEY)
            print(f"LLM service initialized with {LLM_MODEL}")
        except Exception as e:
            print(f"Error initializing LLM service: {e}")
            raise

        self.history = []

        system_prompt = SYSTEM_PROMPTS.get(scenario, SYSTEM_PROMPTS["demo_scheduling"])
        self.history.append(system_prompt)
        self.llm.invoke(self.history)

    def get_response(self, text, max_retries=3):
        if not text:
            return "I didn't catch that. Please try again."
        
        for attempt in range(max_retries):
            try:
                self.history.append(text)
                response = self.llm.invoke(self.history)
                return response.content
            except Exception as e:
                print(f"Error getting AI response (attempt {attempt+1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {2**attempt} seconds...")
                    time.sleep(2**attempt)
                else:
                    return "I'm having trouble processing your request right now. Please try again later."