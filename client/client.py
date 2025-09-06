import asyncio
import websockets

async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello Server from Abhijit!")
        response = await websocket.recv()
        print(f"Server replied: {response}")

if __name__ == "__main__":
    asyncio.run(hello())