import aiofiles
import aiohttp
import asyncio
import requests
import json

async def quet_bai_no_cookie(encoded_post):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': 'datr=oI-xZ60LQVqZq_fibagBnWIz; sb=pI-xZwaEBcMHDJXnF1F-Mctg; wd=842x551; dpr=1.5',
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

