import asyncio

HOST = '127.0.0.1'
PORT = 8888

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"[+] Conexão de {addr}")

    request = await reader.read(1024)
    request_text = request.decode()
    print(f"[{addr}] {request_text.splitlines()[0]}")

    body = """\
<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"><title>Servidor asyncio</title></head>
<body>
<h1>Olá, você se conectou ao servidor asyncio!</h1>
</body>
</html>
"""
    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        "Connection: close\r\n"
        f"Content-Length: {len(body.encode())}\r\n"
        "\r\n"
        + body
    )
    writer.write(response.encode())
    await writer.drain()
    writer.close()
    await writer.wait_closed()
    print(f"[-] Conexão encerrada {addr}")

async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    addr = server.sockets[0].getsockname()
    print(f"Servidor HTTP rodando em {addr}")

    async with server:
        await server.serve_forever()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Servidor finalizado manualmente.")
