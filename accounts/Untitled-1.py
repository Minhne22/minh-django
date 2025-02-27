import asyncio

async def print_user(user):
    while True:
        print(f"User: {user}")
        await asyncio.sleep(1)

# Chạy thử hàm async

