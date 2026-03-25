import asyncio
import random

async def coletar_dados(id_tarefa):
    print(f"Iniciando tarefa {id_tarefa}")
    await asyncio.sleep(random.uniform(0.5, 2))
    return f"dado_{id_tarefa}"

async def main():
    tarefas = [coletar_dados(i) for i in range(1, 6)]
    resultados = await asyncio.gather(*tarefas)
    print(resultados)

asyncio.run(main())