from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json

app = FastAPI()

templates = Jinja2Templates(directory='templates')

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    with open('data.json', mode='r', encoding='utf-8') as f:
        json_data = json.load(f)
    return templates.TemplateResponse("messages.html", {"request": request, 'savedMessages': json_data['messages']})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()

        with open('data.json', mode='r+', encoding='utf-8') as f:
            json_data = json.load(f)
            json_data['messages'].append(data)
            f.seek(0)
            json.dump(json_data, f, indent=4)

        await websocket.send_text(f"Message text: {data}")