import httpx
import aiofiles
import os
import asyncio
import motor.motor_asyncio
import datetime
import random

cache_path = './uid.cache'
if not os.path.exists(cache_path):
    open(cache_path, 'w+', encoding='utf8').close()

uid_cache = open(cache_path, encoding='utf8').read()

# MongoDB Setup
MONGODB_URI = 'mongodb+srv://minhne2203:cCdkU1nRpPsQ07Q8@cluster0.twcco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)


db = client['fb_cmt_manage']
links_collection = db['facebook_links']
comments_collection = db['facebook_comments']
proxies_collection = db['proxies']
cookie_collection = client['store']['cookies']
token_collection = client['store']['tokens']

async def get_list(collection, data={}):
    data = []
    async for document in collection.find(data):
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
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }
    
    session = httpx.AsyncClient(proxy=f'http://{ipport}', headers=headers, follow_redirects=False)
    
    # Get Data
    
    try:
        if link_post.isdigit():
            link_post = f'https://www.facebook.com/{link_post}'
        
        # print(link_post)
        response = await session.get(
            link_post
        )
        # print(response.url)
        # with open('response.html', 'w+', encoding='utf8') as f:
        #     f.write(response.text)
        
        response = response.text
        # print(len(response))
        
        post_id = response.split('"parent_feedback":{"id":"')[1].split('"')[0] if '"parent_feedback":{"id":"' in response \
            else response.split("'parent_feedback': {'id': '")[1].split('\'')[0]
        
        # print(post_id)
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
                uid = await get_uid_num(link_pro5, session)
            
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
        async with aiofiles.open('logs.txt', 'a+', encoding='utf8') as f:
            now = datetime.datetime.now()
            # Định dạng thời gian thành chuỗi
            formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
            await f.write(f'[{formatted_time}] - [No Cookie] - {e}\n')

async def get_by_cookie(link_post, cookie, proxy=''):
    global uid_cache
    # Config Session
    ipport = f'{proxy["ip"]}:{proxy["port"]}' if not proxy['username'] else f'{proxy["username"]}:{proxy["password"]}@{proxy["ip"]}:{proxy["port"]}'
    
    print(ipport)
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=0, i',
        'cookie': cookie,
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }
    
    session = httpx.AsyncClient(proxy=f'http://{ipport}', headers=headers, follow_redirects=False)
    
    # Get Data
    
    try:
        if link_post.isdigit():
            link_post = f'https://www.facebook.com/{link_post}'
        
        print(link_post)
        response = await session.get(
            link_post
        )
        print(response.url)
        # with open('response.html', 'w+', encoding='utf8') as f:
        #     f.write(response.text)
        
        response = response.text
        print(len(response))
        
        post_id = response.split('"parent_feedback":{"id":"')[1].split('"')[0] if '"parent_feedback":{"id":"' in response \
            else response.split("'parent_feedback': {'id': '")[1].split('\'')[0]
        
        print(post_id)
        pid = response.split('"post_id":"')[1].split('"')[0] if '"post_id":"' in response\
            else response.split("'post_id': '")[1].split('\'')[0]
        
        print(pid)
        
        
        user = response.split('"USER_ID":"')[1].split('"')[0] if '"USER_ID":"' in response else \
                response.split("'USER_ID': '")[1].split('\'')[0]
        
        fb_dtsg = response.split('"DTSGInitialData",[],{"token":"')[1].split('"')[0] if '"DTSGInitialData",[],{"token":"' in response else \
                response.split("['DTSGInitialData', [], {'token': '")[1].split('\'')[0]
        
        
        data = {
                'av': user,
                '__aaid': '0',
                '__user': user,
                '__a': '1',
                '__req': '17',
                '__hs': '20083.HYP:comet_loggedout_pkg.2.1.0.0.0',
                'dpr': '1',
                '__ccg': 'EXCELLENT',
                '__rev': '1019077343',
                '__s': 'ew02ta:bsck7x:9vkuon',
                '__hsi': '7452585136370389220',
                'fb_dtsg': fb_dtsg,
                'jazoest': '25507',
                '__comet_req': '15',
                'lsd': 'AVpOnNuOsK0',
                '__spin_r': '1019077343',
                '__spin_b': 'trunk',
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'CommentListComponentsRootQuery',
                'variables': f'{{"commentsIntentToken":"RECENT_ACTIVITY_INTENT_V1","feedLocation":"PERMALINK","feedbackSource":2,"focusCommentID":null,"scale":1,"useDefaultActor":false,"id":"{post_id}","__relay_internal__pv__IsWorkUserrelayprovider":false}}',
                'server_timestamps': 'true',
                'doc_id': '9051058151623566'
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
                uid = await get_uid_num(link_pro5, session)
            
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
        async with aiofiles.open('logs.txt', 'a+', encoding='utf8') as f:
            now = datetime.datetime.now()
            # Định dạng thời gian thành chuỗi
            formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
            await f.write(f'[{formatted_time}] - [Cookie] - {e}\n')

async def get_by_token(id_post, token, proxy=''):
    # Config Session
    ipport = f'{proxy["ip"]}:{proxy["port"]}' if not proxy['username'] else f'{proxy["username"]}:{proxy["password"]}@{proxy["ip"]}:{proxy["port"]}'
    
    session = httpx.AsyncClient(proxy=f'http://{ipport}')
    
    # Get Data
    for _ in range(5):
        try:
            params = {
                'access_token': token,
                'order': 'reverse_chronological',
                'fields': 'created_time,message,id,from'
            }
            response = await session.get(
                f'https://graph.facebook.com/{id_post}/comments',
                params=params
            )
            
            response = response.json()['data'][0]
            print(response)
            await session.aclose()
            return {
                'post_id': id_post,
                'text': response['message'],
                'name': response['from']['name'],
                'time': response['created_time'].split('+')[0].replace('T', ' '),
                'author_id': response['from']['id'],
                'phone': '0'
            }
        except httpx._exceptions.ProxyError:
            await session.aclose()
            proxies_collection.update_one({'ip': proxy['ip'], 'port': str(proxy['port'])}, {'$set': {'status': 'inactive'}})
            return {}
        except httpx._exceptions.ConnectError:
            pass



async def don_luong(indata, proxy):
    link = indata['origin_url']
    data = {}
    
    try:
        if indata['status'] == 'public':
            data = await get_no_cookie(link, proxy=proxy)
            # pass
        else:
            # print(indata)
            # if random.choice([True, False]):
                try:
                    cookie = random.choice(cookies)['cookie']
                    print(cookie)
                    data = await get_by_cookie(link, cookie, proxy=proxy)
                except:
                    await cookie_collection.update_one({'cookie': cookie}, {'$set': {'status': 'inactivate'}})
            # else:
            #     try:
            #         token = random.choice(tokens)['token']
            #         data = await get_by_token(indata['post_id'], token, proxy=proxy)
            #     except:
            #         await token_collection.update_one({'token': token}, {'$set': {'status': 'inactivate'}})
        print(data)
        if data:
            data['origin_url'] = link
            data['content'] = indata['name']
            filter_condition = {
                "post_id": data["post_id"],
                "author_id": data["author_id"],
                "text": data["text"]
            }
            comments_collection.update_one(filter_condition, {"$set": data}, upsert=True)
            links_collection.update_one({"post_id": data["post_id"]}, {"$set": {"last_comment_time": data['time']}})
    except Exception as e:
        async with aiofiles.open('logs.txt', 'a+', encoding='utf8') as f:
            now = datetime.datetime.now()
            # Định dạng thời gian thành chuỗi
            formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
            await f.write(f'[{formatted_time}] - {e}\n')


async def quan_ly_luong():
    while True:
        global proxies, links, cookies, tokens
        # tokens = list(token_collection.find())
        proxies = await get_list(proxies_collection)
        # print(proxies)
        links = await get_list(links_collection)
        # print(links)
        # credentials = [
        #     x for x in tokens for x in tokens if x['status'] == 'live'
        # ]
        cookies = await get_list(cookie_collection, {'status': 'activate'})
        # tokens = await get_list(token_collection, {'status': 'activate'})
        tasks = []
        print(len(links))
        for url in links:
            # print(url)
            # Tạo và thêm các công việc vào danh sách tasks
            tasks.append(don_luong(url, random.choice(proxies)))
        
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

