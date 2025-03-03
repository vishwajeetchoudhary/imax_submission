from app import app

import uvicorn

from prompts.system_prompts import INITIAL_GREETINGS

from config.settings import AUDIO_GREETING_PATH

import threading

def run_backend():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":  # Fixed the main check
    run_backend()