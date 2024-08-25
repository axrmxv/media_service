import asyncio


async def upload_to_cloud(file_path: str, uid: str):
    await asyncio.sleep(1)

    print(f"Файл {uid} загружен в облвко.")
