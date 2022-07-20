from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json

app = FastAPI()

templates = Jinja2Templates(directory='templates')


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("messages.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    i = 0
    await websocket.accept()
    while True:
        i += 1
        data = await websocket.receive_json()
        data['counter'] = i
        await websocket.send_json(data)
