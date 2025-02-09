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
links_collection = db['facebook_links']
comments_collection = db['facebook_comments']

async def don_luong(indata, proxy='', credential=''):
    global uid_cache
    # Config Session
    ipport = f'{proxy["ip"]}:{proxy["port"]}' if not proxy['username'] else f'{proxy["username"]}:{proxy["password"]}@{proxy["ip"]}:{proxy["port"]}'
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'datr=W06SZ_48TKb0XgBDj5NmAmV4; sb=W06SZweBwrhWi9P0gH85_X0b; dpr=1.5; wd=819x551',
        'dpr': '1.5',
        'priority': 'u=0, i',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-full-version-list': '"Not A(Brand";v="8.0.0.0", "Chromium";v="132.0.6834.110", "Google Chrome";v="132.0.6834.110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"19.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'viewport-width': '819',
    }
    
    session = httpx.AsyncClient(proxy=f'http://{ipport}', headers=headers)
    
    