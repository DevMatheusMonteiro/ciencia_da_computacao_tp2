import asyncio

async def coletar():
    await asyncio.sleep(1)
    dado = "dado"
    print("[E1] coletado")
    return dado

async def transformar(dado):
    await asyncio.sleep(5)
    dado = dado.upper()
    print("[E2] transformado")
    return dado

async def enviar(dado):
    await asyncio.sleep(1)
    print(f"[E3] enviado: {dado}")

async def pipeline():
    dado = await coletar()
    dado = await transformar(dado)
    await enviar(dado)

async def main():
    tarefas = [pipeline() for _ in range(3)]
    await asyncio.gather(*tarefas)

asyncio.run(main())
