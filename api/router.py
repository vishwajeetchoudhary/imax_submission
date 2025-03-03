from fastapi import APIRouter, WebSocket, Request,WebSocketDisconnect
from session_manager.session_manager import SessionManager
from config.settings import USER_AUDIO_PATH,AUDIO_GREETING_PATH
from prompts.system_prompts import INITIAL_GREETINGS
from services.speech_service import SpeechService
import json

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    sm = SessionManager()
    if sm:
        text=""
        scenario = sm.get_scenario()
        if(scenario == "1"):
            text = "Namaste! Mai TechSolutions India se bol raha hoon. Kya aap hamare CRM system ke bare mein jaankari lena chahenge?"
        elif(scenario == "2"):
            text = "Namaste! Mai TechSolutions India se bol raha hoon. Hum aapka interview lene wale hain Software Engineering Role ke liye. Kya aap ready hain?"
        elif(scenario == "3"):
            text = "Namaste! Mai TechSolutions India se bol raha hoon. Main aapke pending payment ke vishay mein baat karna chahta hoon."
        audio_file = SpeechService().synthesize_speech(text,AUDIO_GREETING_PATH)
        with open(AUDIO_GREETING_PATH, "rb") as f:
            audio_data = f.read()
            await websocket.send_bytes(audio_data)
    try:
        while True:
            handler = SessionManager().get_handler()
            print(f"Handler: {handler}")
            speech_service = SpeechService()
            data = await websocket.receive_bytes()
            print(f"Received audio data: {len(data)} bytes")

            with open(USER_AUDIO_PATH, "wb") as audio_file:
                audio_file.write(data)

            recognized_text = speech_service.recognize_speech_from_file(USER_AUDIO_PATH)
            print(f"Recognized text: {recognized_text}")

            text_data = {"text": recognized_text,"speaker":"user"}
            await websocket.send_text(json.dumps(text_data))

            if recognized_text and handler:
                ai_response = handler.handle_request(recognized_text)
                print(f"🤖 AI Response: {ai_response}")
                ai_data = {"text": ai_response,"speaker":"bot"}
                await websocket.send_text(json.dumps(ai_data))

                audio_file = speech_service.synthesize_speech(ai_response)
                with open(audio_file, "rb") as f:
                    audio_data = f.read()
                    await websocket.send_bytes(audio_data)
            else:
                print("No handler found or recognized text")
    except WebSocketDisconnect:
        print("WebSocket disconnected. Ending loop.")
    except Exception as e:
        print(f"Error in websocket endpoint: {e}")
    

@router.post("/update")
async def update_scenario(request: Request):
    data = await request.json() 
    scenario = data.get("scenario")
    user_email = data.get("email")

    if not scenario or not user_email:
        return {"error": "Missing required fields"}

    session_manager = SessionManager()
    session_manager.update_handler(scenario, user_email)

    return {"message": "handler updated."}