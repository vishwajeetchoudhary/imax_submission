from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path

from api.router import router

app = FastAPI()

app.mount("/static",StaticFiles(directory="ui"),name="static")

def send_html(filename):
    file_path = Path("ui") / filename
    return file_path.read_text(encoding="utf-8")


app.include_router(router)

@app.get("/",response_class=HTMLResponse)
async def read_root():
    return send_html("index.html")