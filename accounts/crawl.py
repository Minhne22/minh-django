import aiofiles
import aiohttp
import asyncio
import pymongo.collation
import pymongo.collection
import pymongo.typings
import requests
import json
import pymongo
from bs4 import BeautifulSoup 
from lxml import etree
import random
import datetime
import base64

def convert_b64(text: str):
    return base64.b64encode(text.encode()).decode()

loi_cookie = {}
loi_token = {}

user_threads = {}


client = pymongo.AsyncMongoClient('mongodb+srv://minhne2203:cCdkU1nRpPsQ07Q8@cluster0.twcco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
store_credentials = client['store']
cookie_collection = store_credentials['cookies']
token_collection = store_credentials['tokens']
user_comments_collection = client['user_comments']
comments_collection = client['fb_cmt_manage']['facebook_comments']
users_db = client['user_links']



async def quet_bai_no_cookie(encoded_post):
    headers =  {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': 'datr=QYuEZ_z_-ErmElrzCBe57uaW;sb=QYuEZ4lOEbFodz4x2Z-YGvqQ;ps_l=1;ps_n=1;c_user=100034994394353;vpd=v1%3B464x310x2.0000000596046448;wl_cbv=v2%3Bclient_version%3A2738%3Btimestamp%3A1739250308;fbl_st=100622811%3BT%3A28987505;dpr=1.5;ar_debug=1;xs=16%3Amg6IEZfvivGF4A%3A2%3A1737636239%3A-1%3A6328%3ADiOmp6jSAMZSVw%3AAcVIwSh-lypqeTAr_z3-WSK6YdMNBwsvqrla-6OQVHZe;wd=1280x585;fr=131H2fkITpZch6c5R.AWWaGvuRcvuZUz54h474IpuwZFbe_jWYJ9wn5Q.BntG2Z..AAA.0.0.BntHrz.AWWR-JYcGEo;presence=C%7B%22lm3%22%3A%22u.100009453089068%22%2C%22t3%22%3A%5B%7B%22o%22%3A0%2C%22i%22%3A%22u.156025504001094%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22sc.7556805407697542%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.273966199136801%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.100095541452475%22%7D%5D%2C%22utc3%22%3A1739881266345%2C%22v%22%3A1%7D;',
        'origin': 'https://www.facebook.com',
        'priority': 'u=1, i',
        'referer': 'https://www.facebook.com/vtv.periodista/posts/pfbid02qfHM7zzG5VHaPR6KJvZEcdvjpWb6bQh5QFKTSg7q3gcfJFLRacNohKGVbs7omdPAl',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-full-version-list': '"Not A(Brand";v="8.0.0.0", "Chromium";v="132.0.6834.197", "Google Chrome";v="132.0.6834.197"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"19.0.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }

    data = {
        'av': '0',
        '__aaid': '0',
        '__user': '0',
        '__a': '1',
        'dpr': '1',
        '__ccg': 'GOOD',
        '__comet_req': '15',
        'lsd': '',
        'jazoest': '',
        '__spin_b': 'trunk',
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': 'CommentListComponentsRootQuery',
        'variables': '{"commentsIntentToken":"RECENT_ACTIVITY_INTENT_V1","feedLocation":"DEDICATED_COMMENTING_SURFACE","feedbackSource":110,"focusCommentID":null,"scale":1,"useDefaultActor":false,"id":"' + encoded_post + '","__relay_internal__pv__IsWorkUserrelayprovider":false}',
        'server_timestamps': 'true',
        'doc_id': '9051058151623566',
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post('https://www.facebook.com/api/graphql/', headers=headers, data=data) as response:
            response_text = await response.text()
            try:
                response_json = json.loads(response_text)
                if not response_json['data']['node']:
                    print(encoded_post)

                comment = response_json['data']['node']['comment_rendering_instance_for_feed_location']['comments']['edges'][0]
                info = comment['node']
                comment_count = response_json['data']['node']['comment_rendering_instance']['comments']['total_count']
                pid = response_text.split('"post_id":"')[1].split('"')
                data = {
                    'post_id': pid,
                    'text': info['body']['text'],
                    'name': info['author']['name'],
                    'time': info['comment_action_links'][0]['comment']['created_time'],
                    'author_id': info['discoverable_identity_badges_web'][0]['serialized'].split('actor_id')[1].split(':')[1].split(',')[0],
                    'phone': '0',
                    'comment_count': comment_count
                }
            except json.JSONDecodeError:
                print("Failed to parse JSON")
                return None

async def quet_bai_cookie(encoded_post, cookie):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': cookie,
        'origin': 'https://www.facebook.com',
        'priority': 'u=1, i',
        'referer': 'https://www.facebook.com/vtv.periodista/posts/pfbid02qfHM7zzG5VHaPR6KJvZEcdvjpWb6bQh5QFKTSg7q3gcfJFLRacNohKGVbs7omdPAl',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-full-version-list': '"Not A(Brand";v="8.0.0.0", "Chromium";v="132.0.6834.197", "Google Chrome";v="132.0.6834.197"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"19.0.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }

    data = {
        'av': '0',
        '__aaid': '0',
        '__user': '0',
        '__a': '1',
        'dpr': '1',
        '__ccg': 'GOOD',
        '__comet_req': '15',
        'lsd': '',
        'jazoest': '',
        '__spin_b': 'trunk',
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': 'CommentListComponentsRootQuery',
        'variables': '{"commentsIntentToken":"RECENT_ACTIVITY_INTENT_V1","feedLocation":"DEDICATED_COMMENTING_SURFACE","feedbackSource":110,"focusCommentID":null,"scale":1,"useDefaultActor":false,"id":"' + encoded_post + '","__relay_internal__pv__IsWorkUserrelayprovider":false}',
        'server_timestamps': 'true',
        'doc_id': '9051058151623566',
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post('https://www.facebook.com/api/graphql/', headers=headers, data=data) as response:
            response_text = await response.text()
            try:
                response_json = json.loads(response_text)
                comment = response_json['data']['node']['comment_rendering_instance_for_feed_location']['comments']['edges'][0]
                info = comment['node']
                comment_count = response_json['data']['node']['comment_rendering_instance']['comments']['total_count']
                pid = response_text.split('"post_id":"')[1].split('"')
                data = {
                    'post_id': pid,
                    'text': info['body']['text'],
                    'name': info['author']['name'],
                    'time': info['comment_action_links'][0]['comment']['created_time'],
                    'author_id': info['discoverable_identity_badges_web'][0]['serialized'].split('actor_id')[1].split(':')[1].split(',')[0],
                    'phone': '0',
                    'comment_count': comment_count
                }
            except json.JSONDecodeError:
                print("Failed to parse JSON")
                return None

async def quet_bai_token(id_post, token):
    params = {
        'summary': '1',
        'limit': '1',
        'order': 'reverse_chronological',
        'fields': 'created_time,message,id,from'
    }


async def get_user_info(user_url, cookie):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': cookie,
        'dpr': '1.5',
        'priority': 'u=0, i',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-full-version-list': '"Not A(Brand";v="8.0.0.0", "Chromium";v="132.0.6834.197", "Google Chrome";v="132.0.6834.197"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"19.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'viewport-width': '842',
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url=user_url, headers=headers, allow_redirects=True) as response:
            response = await response.text()
            with open('hi.html', 'w+', encoding='utf8') as f:
                f.write(response)
            try:
                soup = BeautifulSoup(response, "html.parser") 
                for ele in soup.find_all():
                    if 'Giới thiệu' == ele.text:
                        db = ele.find_next_sibling()
                        z = db.text
                print(z)
                user_id = response.split('"userID":"')[1].split('"')[0]
                user_name = response.split('"data":{"name":"')[1].split('"')[0].encode().decode('unicode_escape')
                
                return {
                    'id': user_id,
                    'name': user_name,
                    'info': '\n'.join([])
                }
            except Exception as e:
                print(e)
                return None


async def don_luong(indata, collection, delay=5):
    print(indata)
    post_id = indata['post_id']
    encoded_post = indata['encoded_post'] if 'encoded_post' in indata else convert_b64(f'feedback:{post_id}')

    status: str = indata['status']
    post_id: str = indata['post_id']
    cookie_input = {}
    token = ''
    while True:
        # try:
            if status == 'public':
                response = await quet_bai_no_cookie(encoded_post)
            elif status == 'private':
                if random.randint(0, 1):
                    try:
                        response = await quet_bai_cookie(encoded_post, cookie_input)
                        loi_cookie[cookie_input['cookie']] = 0
                    except:
                        loi_cookie[cookie_input['cookie']] += 1
                        if loi_cookie[cookie_input['cookie']] > 5:
                            await cookie_collection.delete_one({"cookie": cookie_input['cookie']})
                        
                    
                else:
                    try:
                        response = await quet_bai_token(post_id, token)
                        loi_token[token] = 0
                    except:
                        loi_token[token] += 1
                        if loi_token[token] > 5:
                            await token_collection.delete_one({"token": loi_token[token]})
            else:
                return
            data = response
            filter_condition = {
                "post_id": data["post_id"],
                "author_id": data["author_id"],
                "text": data["text"]
            }
            print(data)
            await collection.update_on(filter_condition, {"$set": data}, upsert=True)
        # except Exception as e:
        #     async with aiofiles.open('logs - crawl.txt', 'a+', encoding='utf8') as f:
        #         now = datetime.datetime.now()
        #         # Định dạng thời gian thành chuỗi
        #         formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
        #         await f.write(str(e) + '\n')
        # print('Ok')
            await asyncio.sleep(delay)

async def khoi_tao_luong():
    existing_data = []
    tasks = []
    # while True:
    await quan_ly_luong(existing_data=existing_data, tasks=tasks)
        # await asyncio.sleep(10)

async def quan_ly_luong(existing_data, tasks):
    print(existing_data, tasks)
    users = await users_db.list_collection_names()
    print(users)
    cookies = [
        x async for x in cookie_collection.find({'status': 'active'})
    ]
    tokens = [
        x async for x in token_collection.find({'status': 'active'})
    ]
    
    for username in users:
        posts = users_db[username].find({'active': 'on'})
        async for post in posts:
            post_id = post['post_id']
            data = f'{username}_{post_id}'
            if data not in existing_data:
                print('new')
                existing_data.append(existing_data)
                collection = user_comments_collection[username]
                task = asyncio.create_task(don_luong(indata=post, collection=collection, delay=post['delay'] if 'delay' in post else 5))
                tasks.append(task)
    print('+'*15)
    await asyncio.gather(*tasks)


        

asyncio.run(khoi_tao_luong())