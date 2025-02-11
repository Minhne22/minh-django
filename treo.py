import httpx
import aiofiles
import os
import asyncio
import motor.motor_asyncio
import datetime
import random
import aiohttp

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
proxies_collection = db['proxies']

async def get_list(collection):
    data = []
    async for document in collection.find():
        data.append(document)
    return data

async def get_uid_num(link_pro5, session):
    
    # Check if UID is in cache
    if link_pro5 in uid_cache:
        uid = uid_cache.split(f'{link_pro5}|')[1].split('\n')[0]
        return uid

    response = await session.get(f'https://www.facebook.com/{link_pro5}')
    response_text = response.text

    if 'fb://profile/' in response_text:
        uid = response_text.split('fb://profile/')[1].split('"')[0]
        return uid
    
    else:
        data = {
            'link': f'https://www.facebook.com/{link_pro5}',
        }
        while True:
            response = await session.post('https://id.traodoisub.com/api.php', data=data)
            response = response.json()
            if 'id' not in response:
                await asyncio.sleep(3)
                print('Get lai ID')
            else:
                print('Done')
                return response['id']
    

async def get_no_cookie(link_post, proxy=''):
    global uid_cache
    # Config Session
    ipport = f'{proxy["ip"]}:{proxy["port"]}' if not proxy['username'] else f'{proxy["username"]}:{proxy["password"]}@{proxy["ip"]}:{proxy["port"]}'
    
    print(ipport)
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'datr=6S6rZ5IQrMtHuaXZ_-KVi7r8; sb=6S6rZ-2aG-29dBs6Q-6Ep9FW; dpr=1.5; wd=935x612',
        'origin': 'https://www.facebook.com',
        'priority': 'u=1, i',
        'referer': 'https://www.facebook.com/100085020425798/videos/1464735244237949/',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-full-version-list': '"Not A(Brand";v="8.0.0.0", "Chromium";v="132.0.6834.160", "Google Chrome";v="132.0.6834.160"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"19.0.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        # 'x-asbd-id': '129477',
        # 'x-fb-lsd': 'AVrmtdx-RxI',
    }
    
    session = httpx.AsyncClient(proxy=f'http://{ipport}', headers=headers, follow_redirects=True)
    
    # Get Data
    
    try:
        if link_post.isdigit():
            link_post = f'https://www.facebook.com/{link_post}'
        
        print(link_post)
        response = await session.get(
            link_post
        )
        print(response.url)
        with open('response.html', 'w+', encoding='utf8') as f:
            f.write(response.text)
        
        response = response.text
        print(len(response))
        
        post_id = response.split('"parent_feedback":{"id":"')[1].split('"')[0] if '"parent_feedback":{"id":"' in response \
            else response.split("'parent_feedback': {'id': '")[1].split('\'')[0]
        
        print(post_id)
        pid = response.split('"post_id":"')[1].split('"')[0] if '"post_id":"' in response\
            else response.split("'post_id': '")[1].split('\'')[0]
        
        print(pid)
        
        
        lsd = response.split('"LSD",[],{"token":"')[1].split('"')[0] if '"LSD",[],{"token":"' in response else \
                response.split("['LSD', [], {'token': '")[1].split('\'')[0]
        
        data = {
            'av': '0',
            '__aaid': '0',
            '__user': '0',
            '__a': '1',
            '__req': 's',
            '__hs': '',
            'dpr': '1',
            '__ccg': 'GOOD',
            '__rev': '',
            '__s': '',
            '__hsi': '',
            '__dyn': '',
            '__csr': '',
            '__comet_req': '15',
            'lsd': lsd,
            'jazoest': '2914',
            '__spin_r': '',
            '__spin_b': '',
            '__spin_t': '',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'CommentListComponentsRootQuery',
            'variables': '{"commentsIntentToken":"RECENT_ACTIVITY_INTENT_V1","feedLocation":"TAHOE","feedbackSource":2,"focusCommentID":null,"scale":1,"useDefaultActor":false,"id":"' + post_id + '","__relay_internal__pv__IsWorkUserrelayprovider":false}',
            'server_timestamps': 'true',
            'doc_id': '8894656107282580',
        }
        
        response = await session.post(
            'https://www.facebook.com/api/graphql/',
            data=data
        )
        
        response = response.json()
        
        comment = response['data']['node']['comment_rendering_instance_for_feed_location']['comments']['edges'][0]
        
        info = comment['node']
        try: 
            data = {
                'post_id': pid,
                'text': info['body']['text'],
                'name': info['author']['name'],
                'time': info['comment_action_links'][0]['comment']['created_time'],
                'author_id': info['discoverable_identity_badges_web'][0]['serialized'].split('actor_id')[1].split(':')[1].split(',')[0],
                'phone': '0'
            }
            
        
        except IndexError:
            link_pro5 = str(info['author']['id'])
            if link_pro5.isnumeric():
                uid = link_pro5
            else:
                uid = await get_uid_num(link_pro5)
            
            uid_cache += f'{link_pro5}|{uid}\n'
            with open('./uid.cache', 'w+', encoding='utf8') as f:
                f.write(uid_cache)
            
            data = {
                'post_id': pid,
                'text': info['body']['text'],
                'name': info['author']['name'],
                'time': info['comment_action_links'][0]['comment']['created_time'],
                'author_id': uid,
                'phone': '0'
            }
            
        await session.aclose()
            
        return data
        
    
    except Exception as e:
        print(e)
        await session.aclose()
    
async def don_luong(link, proxy):
    try:
        data = await get_no_cookie(link, proxy=proxy)
        print(data)
        if data:
            filter_condition = {"post_id": data["post_id"]}
            comments_collection.update_one(filter_condition, {"$set": data}, upsert=True)
    except Exception as e:
        async with aiofiles.open('logs.txt', 'a+', encoding='utf8') as f:
            now = datetime.datetime.now()
            # Định dạng thời gian thành chuỗi
            formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
            await f.write(f'[{formatted_time}] - {e}\n')
    

async def quan_ly_luong():
    while True:
        global proxies, links, credentials
        # tokens = list(token_collection.find())
        proxies = await get_list(proxies_collection)
        print(proxies)
        links = await get_list(links_collection)
        print(links)
        # credentials = [
        #     x for x in tokens for x in tokens if x['status'] == 'live'
        # ]
        tasks = []
        print(len(links))
        for url in links:
            # print(url)
            # Tạo và thêm các công việc vào danh sách tasks
            tasks.append(don_luong(url['post_id'], random.choice(proxies)))
        
        # Chờ tất cả các công việc trong tasks hoàn thành
        await asyncio.gather(*tasks)
        await asyncio.sleep(time_delay)
                
def start_background_task():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(quan_ly_luong())
    loop.run_forever()

time_delay = 5
start_background_task()