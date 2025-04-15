import httpx
import asyncio


async def register_user():
    register_url = "http://127.0.0.1:8000/api/v1/register/"
    register_data = {
        "username": "admin3",
        "email": "admin3@example.com",
        "password": "admin3"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(register_url, json=register_data)
        response.raise_for_status()
        return response.json()


# Запуск асинхронной функции
asyncio.run(register_user())