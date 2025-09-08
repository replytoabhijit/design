import asyncio
import itertools

LISTEN_HOST= "0.0.0.0"
LISTEN_PORT= 9000
BACKENDS = [("127.0.0.1", 9001), ("127.0.0.1", 9002)]

backend_cycle = itertools.cycle(BACKENDS)

async def requestHandler(client_reader: asyncio.StreamReader, client_writer: asyncio.StreamWriter):
    """Handle incoming client connection and forward to a backend"""
    client_addr = client_writer.get_extra_info("peername")
    backend_host, backend_port = next(backend_cycle)

    try:
        backend_reader, backend_writer = await asyncio.open_connection(
            host=backend_host, port=backend_port
        )
        print(f"Forwarding request from {client_addr} to backend: {backend_host}:{backend_port}")

        async def forward(reader, writer, direction):
            """Pipe data between sockets"""
            try:
                while True:
                    data = await reader.read(4096)
                    if not data:
                        break
                    writer.write(data)
                    await writer.drain()
            except Exception as e:
                print(f"⚠️ Connection error {direction}: {e}")
            finally:
                writer.close()
                await writer.wait_closed()

        # Forward request from client to backend
        asyncio.create_task(forward(client_reader, backend_writer, "client->backend"))
        # Forward response from backend to client
        asyncio.create_task(forward(backend_reader, client_writer, "backend->client"))
    except Exception as e:
        print(f"Error: {e}")
        client_writer.close()

    

async def main():
    print(f"Starting load balancer on {LISTEN_HOST}:{LISTEN_PORT}, forwarding to backends: {BACKENDS}")
    server = await asyncio.start_server(requestHandler, LISTEN_HOST, LISTEN_PORT)
    addr = server.sockets[0].getsockname()
    print(f"Load Balancer listening on {addr}, forwarding to backends: {BACKENDS}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
    # asyncio.run(asyncio.start_server(
    #     lambda r, w: asyncio.create_task(
    #         asyncio.start_server(
    #             lambda br, bw: asyncio.create_task(
    #                 asyncio.gather(
    #                     asyncio.create_task(pipe(r, bw)),
    #                     asyncio.create_task(pipe(br, w))
    #                 )
    #             ),
    #             backend_cycle.__next__()["host"],
    #             backend_cycle.__next__()["port"]
    #         ).then(lambda s: s.serve_forever())
    #     ),
    #     LISTEN_HOST,
    #     LISTEN_PORT
    # ).serve_forever())