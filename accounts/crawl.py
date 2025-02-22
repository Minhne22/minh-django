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
import os

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

cache_path = './uid.cache'
if not os.path.exists(cache_path):
    open(cache_path, 'w+', encoding='utf8').close()

uid_cache = open(cache_path, encoding='utf8').read()

async def get_uid_num(link_pro5):
    global uid_cache
    
    # Check if UID is in cache
    if link_pro5 in uid_cache:
        uid = uid_cache.split(f'{link_pro5}|')[1].split('\n')[0]
        return uid
    async with aiohttp.ClientSession() as session:
    
        # response = await session.get(f'https://www.facebook.com/{link_pro5}')
        # response_text = response.text()
        async with session.get(f'https://www.facebook.com/{link_pro5}') as response:
            response_text = await response.text()
            

            if 'fb://profile/' in response_text:
                uid = response_text.split('fb://profile/')[1].split('"')[0]
                uid_cache += f'{link_pro5}|{uid}\n'
                with open('./uid.cache', 'w+', encoding='utf8') as f:
                    f.write(uid_cache)
                return uid
            
            else:
                data = {
                    'link': f'https://www.facebook.com/{link_pro5}',
                }
                while True:
                    # response = await session.post('https://id.traodoisub.com/api.php', data=data)
                    # response = response.json()
                    async with session.get(f'https://www.facebook.com/{link_pro5}') as response:
                        response = await response.text()
                        if 'id' not in response:
                            await asyncio.sleep(3)
                            print('Get lai ID')
                        else:
                            print('Done')
                            uid = response['id']
                            uid_cache += f'{link_pro5}|{uid}\n'
                            with open('./uid.cache', 'w+', encoding='utf8') as f:
                                f.write(uid_cache)
                            return uid
    

async def quet_bai_no_cookie(encoded_post, proxy={}):
    if proxy:
        ipport = f'{proxy["ip"]}:{proxy["port"]}' if not proxy['username'] else f'{proxy["username"]}:{proxy["password"]}@{proxy["ip"]}:{proxy["port"]}'
        ipport = f'http://{ipport}'
    else:
        ipport = ''
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
    print('Ok')
    
    async with aiohttp.ClientSession() as session:
        async with session.post('https://www.facebook.com/api/graphql/', headers=headers, data=data, proxy=ipport) as response:
            response_text = await response.text()
            # print(response_text)
            # with open('se.json', 'w+', encoding='utf8') as f:
            #             f.write(response_text)
            try:
                response_json = json.loads(response_text)
                # with open('sech.json', 'w+', encoding='utf8') as f:
                #         f.write(response_text)
                comment = response_json['data']['node']['comment_rendering_instance_for_feed_location']['comments']['edges'][0]
                info = comment['node']
                comment_count = response_json['data']['node']['comment_rendering_instance']['comments']['total_count']
                pid = response_text.split('"post_id":"')[1].split('"')[0]
                try: 
                    data = {
                        'post_id': pid,
                        'text': info['body']['text'],
                        'name': info['author']['name'],
                        'time': info['comment_action_links'][0]['comment']['created_time'],
                        'author_id': info['discoverable_identity_badges_web'][0]['serialized'].split('actor_id')[1].split(':')[1].split(',')[0],
                        'phone': '0',
                        'comment_count': comment_count
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
                        'phone': '0',
                        'comment_count': comment_count
                        
                    }
                        
                return data

            except Exception as e:
                print(e)

async def quet_bai_cookie(encoded_post, cookie_inp, proxy={}):
    # print(cookie_inp)
    if proxy:
        ipport = f'{proxy["ip"]}:{proxy["port"]}' if not proxy['username'] else f'{proxy["username"]}:{proxy["password"]}@{proxy["ip"]}:{proxy["port"]}'
        ipport = f'http://{ipport}'
    else:
        ipport = ''
    cookie = cookie_inp['cookie']
    fb_dtsg = cookie_inp['fb_dtsg']
    user_id = cookie_inp['user_id']
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
        'av': user_id,
        '__aaid': '0',
        '__user': user_id,
        '__a': '1',
        '__req': '',
        '__hs': '',
        'dpr': '',
        '__ccg': 'EXCELLENT',
        '__rev': '',
        '__s': '',
        '__hsi': '',
        '__dyn': '',
        '__csr': '',
        '__comet_req': '15',
        'fb_dtsg': fb_dtsg,
        'jazoest': '25628',
        'lsd': '',
        '__spin_r': '1020251702',
        '__spin_b': 'trunk',
        '__spin_t': '1740053623',
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': 'CommentListComponentsRootQuery',
        'variables': '{"commentsIntentToken":"RECENT_ACTIVITY_INTENT_V1","feedLocation":"DEDICATED_COMMENTING_SURFACE","feedbackSource":110,"focusCommentID":null,"scale":1,"useDefaultActor":false,"id":"' + encoded_post + '","__relay_internal__pv__IsWorkUserrelayprovider":false}',
        'server_timestamps': 'true',
        'doc_id': '9051058151623566',
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post('https://www.facebook.com/api/graphql/', headers=headers, data=data, proxy=ipport) as response:
            response_text = await response.text()
            # with open('sech.json', 'w+', encoding='utf8') as f:
            #             f.write(response_text)
            try:
                response_json = json.loads(response_text)
                # with open('sech.json', 'w+', encoding='utf8') as f:
                #         f.write(response_text)
                comment = response_json['data']['node']['comment_rendering_instance_for_feed_location']['comments']['edges'][0]
                info = comment['node']
                comment_count = response_json['data']['node']['comment_rendering_instance']['comments']['total_count']
                pid = response_text.split('"post_id":"')[1].split('"')[0]
                try: 
                    data = {
                        'post_id': pid,
                        'text': info['body']['text'],
                        'name': info['author']['name'],
                        'time': info['comment_action_links'][0]['comment']['created_time'],
                        'author_id': info['discoverable_identity_badges_web'][0]['serialized'].split('actor_id')[1].split(':')[1].split(',')[0],
                        'phone': '0',
                        'comment_count': comment_count
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
                        'phone': '0',
                        'comment_count': comment_count
                        
                    }
                        
                return data
            except json.JSONDecodeError:
                print("Failed to parse JSON")
                raise ('Loi!')
            except Exception as e:
                print(e)

async def quet_bai_token(id_post, token, proxy={}):
    params = {
        # 'summary': '1',
        # 'limit': '1',
        # 'order': 'reverse_chronological',
        'fields': 'comments.limit(1).summary(1).order(reverse_chronological).fields(created_time,message,id,from)',
        'access_token': token
    }
    
    if proxy:
        ipport = f'{proxy["ip"]}:{proxy["port"]}' if not proxy['username'] else f'{proxy["username"]}:{proxy["password"]}@{proxy["ip"]}:{proxy["port"]}'
        ipport = f'http://{ipport}'
    else:
        ipport = ''
    
    url = f'https://graph.facebook.com/v22.0/{id_post}'
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=params, proxy=ipport) as response:
            response = await response.text()
            response = json.loads(response)
            print(response)
            comment = response['comments']['data'][0]
            return {
                'post_id': id_post,
                'text': comment['message'],
                'name': comment['from']['name'],
                'time': int(datetime.datetime.strptime(comment['created_time'], "%Y-%m-%dT%H:%M:%S%z").timestamp()),
                'author_id': comment['from']['id'],
                'phone': '0'
            }
            


# async def get_user_info(user_url, cookie):
#     headers = {
#         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#         'accept-language': 'en-US,en;q=0.9',
#         'cookie': cookie,
#         'dpr': '1.5',
#         'priority': 'u=0, i',
#         'sec-ch-prefers-color-scheme': 'light',
#         'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
#         'sec-ch-ua-full-version-list': '"Not A(Brand";v="8.0.0.0", "Chromium";v="132.0.6834.197", "Google Chrome";v="132.0.6834.197"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-model': '""',
#         'sec-ch-ua-platform': '"Windows"',
#         'sec-ch-ua-platform-version': '"19.0.0"',
#         'sec-fetch-dest': 'document',
#         'sec-fetch-mode': 'navigate',
#         'sec-fetch-site': 'none',
#         'sec-fetch-user': '?1',
#         'upgrade-insecure-requests': '1',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
#         'viewport-width': '842',
#     }
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url=user_url, headers=headers, allow_redirects=True) as response:
#             response = await response.text()
#             # with open('hi.html', 'w+', encoding='utf8') as f:
#             #     f.write(response)
#             try:
#                 soup = BeautifulSoup(response, "html.parser") 
#                 for ele in soup.find_all():
#                     if 'Giới thiệu' == ele.text:
#                         db = ele.find_next_sibling()
#                         z = db.text
#                 # print(z)
#                 user_id = response.split('"userID":"')[1].split('"')[0]
#                 user_name = response.split('"data":{"name":"')[1].split('"')[0].encode().decode('unicode_escape')
                
#                 return {
#                     'id': user_id,
#                     'name': user_name,
#                     'info': '\n'.join([])
#                 }
#             except Exception as e:
#                 print(e)
#                 return None


async def don_luong(indata, collection, delay=5):
    # print(indata)
    global loi_cookie, loi_token
    post_id = indata['post_id']
    encoded_post = convert_b64(f'feedback:{post_id}')

    status: str = indata['status']
    post_id: str = indata['post_id']
    while True:
        try:
            if status == 'public':
                response = await quet_bai_no_cookie(encoded_post)
            elif status == 'private':
                if random.randint(0, 1):
                    try:
                        cookie_input = random.choice(cookies)
                        response = await quet_bai_cookie(encoded_post, cookie_input)
                        loi_cookie[cookie_input['cookie']] = 0
                    except Exception as e:
                        print(e)
                        ck = cookie_input['cookie']
                        if ck not in loi_cookie:
                            loi_cookie[ck] = 0
                        loi_cookie[ck] += 1
                        if loi_cookie[ck] > 5:
                            await cookie_collection.update_one({"cookie": ck}, {'$set': {
                                'status': 'inactive'
                            }})
                        
                    
                else:
                    try:
                        token = random.choice(tokens)['token']
                        
                        response = await quet_bai_token(post_id, token)
                        loi_token[token] = 0
                    except:
                        if token not in loi_token:
                            loi_token[token] = 0
                        print("loi token")
                        loi_token[token] += 1
                        if loi_token[token] > 5:
                            await token_collection.update_one({"token": loi_token[token]}, {'$set': {
                                'status': 'inactive'
                            }})
            else:
                return
            data = response
            if data:
                print(data)
                filter_condition = {
                    "post_id": data["post_id"],
                    "author_id": data["author_id"],
                    "text": data["text"]
                }
                # print(data)
                await collection.update_one(filter_condition, {"$set": data}, upsert=True)
        except Exception as e:
            async with aiofiles.open('logs - crawl.txt', 'a+', encoding='utf8') as f:
                now = datetime.datetime.now()
                # Định dạng thời gian thành chuỗi
                formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
                await f.write(str(e) + '\n')
            print('Ok')
        await asyncio.sleep(delay)

async def khoi_tao_luong():
    existing_data = []
    tasks = []
    while True:
        await quan_ly_luong(existing_data=existing_data, tasks=tasks)
        # await asyncio.sleep(10)

async def quan_ly_luong(existing_data, tasks):
    global cookies, tokens
    # print(existing_data, tasks)
    users = await users_db.list_collection_names()
    # print(users)
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
                # await collection.update_one({'id': '0'}, {"$set": {'test': '1'}}, upsert=True)

                task = asyncio.create_task(don_luong(indata=post, collection=collection, delay=post['delay'] if 'delay' in post else 5))
                tasks.append(task)
    print('+'*15)
    await asyncio.gather(*tasks)


asyncio.run(khoi_tao_luong())

# print(asyncio.run(quet_bai_cookie('ZmVlZGJhY2s6MTIyMTE3NzE5NjQ2NDU3NDA1', {"_id":{"$oid":"67b9c86aef9028e4f5bad88a"},"cookie":"fr=1DJhx1kZMkPsLXLhb.AWVgKAzCvfxZlGq1PxRIiJ82hXc.BnKQEO..AAA.0.0.Bnj0qM.AWVSY9I_RIg;c_user=61551628542882;datr=IcZSZlfNhS0_Gc0dFn7Bizjq;sb=IcZSZlPR15SoYze-eJCTchDH;m_pixel_ratio=1;presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1737443984764%2C%22v%22%3A1%7D;wd=146x150;xs=20%3A1rYeM0hdW6xH_Q%3A2%3A1737443977%3A-1%3A1621;ps_n=1;ps_l=1;","fb_dtsg":"NAcNHuAkSZNnr92YrDWLnSQpJeUY1jutbvCK5cbUyphJ46MT2FR_o9A:20:1737443977","name":"Ndinani Dalot","status":"active","user_id":"61551628542882"})))

# print(asyncio.run(quet_bai_token('1101587491555483', 'EAAAAUaZA8jlABO0T11Fke5FhL5AVruZButRNyZCqXt8drjajdEZCCZAWtT4VKixFRFEqti20c3oQrj52ywEoPZB8jhgTUnE839p4zvDC6pInuGZAmgDZBNIQYZAZB0AJaddotCTP8UuYExWO59oDnwsoaX78qpzZCSkK7Xms0jETBBK43vjYNWxqlFGANHqtgZDZD', {"_id":{"$oid":"67ab33888e74a49fae41b2ff"},"ip":"42.96.5.233","port":"15643","username":"tuanlee15643","password":"lg43k","status":"active"})))