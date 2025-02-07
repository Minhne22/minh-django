import httpx
import aiofiles
import os
import asyncio
import motor.motor_asyncio

cache_path = './cache.txt'
if not os.path.exists(cache_path):
    open(cache_path, 'w+', encoding='utf8').close()

cache = [x for x in open(cache_path, encoding='utf8').read().split('\n') if x]

# MongoDB Setup
MONGODB_URI = 'mongodb+srv://minhne2203:cCdkU1nRpPsQ07Q8@cluster0.twcco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)


db = client['fb_cmt_manage']
fb_collection = db['facebook_links']

async def find_document():
    result = fb_collection.find()
    return [
        x async for x in result
    ]

print(asyncio.run(find_document()))