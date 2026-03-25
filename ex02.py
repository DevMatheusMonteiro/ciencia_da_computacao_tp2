import asyncio
import time

def funcao_custosa():
    print("Iniciando função custosa...")
    time.sleep(3)
    print("Finalizando função custosa...")

async def contador():
    for i in range(5, -1, -1):
        print(f"Contador {i}")
        await asyncio.sleep(1)

async def sem_thread():
    print("\n--- Sem asyncio.to_thread ---")
    tarefa = asyncio.create_task(contador())
    funcao_custosa()
    await tarefa

async def com_thread():
    print("\n--- Com asyncio.to_thread ---")
    tarefa = asyncio.create_task(contador())
    await asyncio.to_thread(funcao_custosa)
    await tarefa

async def main():
    await sem_thread()
    await com_thread()

asyncio.run(main())