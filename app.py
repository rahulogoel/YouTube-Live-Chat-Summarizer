from fastapi import FastAPI, WebSocket, Query
from chat_handler import get_live_chat
from summarizer import summarize_messages
from chat_fetcher import get_live_chat

app = FastAPI()


import asyncio
from starlette.websockets import WebSocketDisconnect

@app.websocket("/ws")
async def chat_summary(websocket: WebSocket, video_id: str = Query(...)):
    await websocket.accept()
    print("WebSocket connected")
    try:
        chat_batches = []
        while True:
            # fetch chat messages and store them
            for chat_batch in get_live_chat(video_id):
                if chat_batch:
                    chat_batches.extend(chat_batch)
            
            # wait for 10 seconds before sending an updated summary
            await asyncio.sleep(10)

            # summarize and send to the client
            if chat_batches:
                summary = summarize_messages(chat_batches)
                await websocket.send_text(summary)
                # clear the batch after summarizing
                chat_batches.clear()

    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"Error in WebSocket handler: {e}")
    finally:
        await websocket.close()


@app.get("/")
def read_root():
    return {"message": "YouTube Chat Summarizer is running."}

@app.websocket("/ws")
async def chat_summary(websocket: WebSocket, video_id: str = Query(...)):
    await websocket.accept()
    try:
        for chat_batch in get_live_chat(video_id):
            if chat_batch:
                summary = summarize_messages(chat_batch)
                await websocket.send_text(summary)
    except Exception as e:
        print(f"Error: {e}")
        await websocket.close()
