from google.cloud import texttospeech
from dotenv import load_dotenv
import os

load_dotenv()

OPEN_AI_KEY = os.environ.get("OPEN_AI_API_KEY")
SERVICE_ACCOUNT_FILE = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

LLM_MODEL = "gpt-4.5-preview"

DEFAULT_LANGUAGE_CODE = "en-IN"

AUDIO_OUTPUT_PATH="audio_data/response.mp3"
AUDIO_GREETING_PATH="audio_data/initial_greeting.mp3"
USER_AUDIO_PATH="audio_data/user_audio.mp3"

DEFAULT_SPEECH_GENDER = texttospeech.SsmlVoiceGender.MALE

SCOPES = ["https://www.googleapis.com/auth/calendar"]

CRM_DATA_DIR = "crm_data"

CALENDAR_ID = "primary"
TIMEZONE = "Asia/Kolkata"


