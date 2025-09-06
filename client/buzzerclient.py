import asyncio
import websockets
import keyboard

async def send_buzz():
    async with websockets.connect("ws://localhost:8765") as websocket:
        await websocket.send("buzz")
        response = await websocket.recv()
        print(f"Server response: {response}")

if __name__ == "__main__":
    asyncio.run(send_buzz())