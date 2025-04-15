import httpx
import asyncio

async def get_jwt_tokens():
    auth_url = "http://127.0.0.1:8000/api/v1/login/"
    auth_data = {
        "username": "admin",
        "password": "admin"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(auth_url, json=auth_data)
        response.raise_for_status()
        return response.json()

# Правильный способ вызова асинхронной функции
async def main():
    token = await get_jwt_tokens()
    print(token)

# Запуск асинхронного кода
asyncio.run(main())