import asyncio
import websockets   

clients = []

async def handle_message(websocket):
    global clients
    global fastest_time
    message = await websocket.recv()
    if message == "buzz":
        response_time = asyncio.get_event_loop().time()
        clients.append((websocket, response_time))
        if len(clients) == 1:
            fastest_time = response_time
            await websocket.send("You are the fastest!")
        else:
            t = round(response_time - fastest_time, 2)
            await websocket.send(f"You were {t} seconds slower than the fastest buzzer.")

async def main():
    async with websockets.serve(handle_message, "localhost", 8765):
        print("WebSocket server running at ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())