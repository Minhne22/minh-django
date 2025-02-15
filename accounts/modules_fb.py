import requests
import random
from datetime import datetime, timezone, timedelta
import re

def get_publish_time(text: str) -> int:
    match = re.search(r'(?:\"|\\\")publish_time(?:\"|\\\")\s*:\s*(\d+)', text)
    if match:
        return int(match.group(1))
    return None


def convert_to_utc7(iso_time: str) -> str:
    # Chuyển đổi chuỗi ISO thành đối tượng datetime
    dt = datetime.strptime(iso_time, "%Y-%m-%dT%H:%M:%S%z")
    
    # Chuyển sang múi giờ UTC+7
    dt_utc7 = dt.astimezone(timezone(timedelta(hours=7)))
    
    # Định dạng theo yêu cầu
    return dt_utc7.strftime("%H:%M:%S %Y/%m/%d")

def timestamp_to_str(timestamp: int) -> str:
    # Chuyển đổi timestamp thành datetime có timezone UTC
    dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    
    # Định dạng lại thời gian
    return dt.strftime("%H:%M:%S %Y/%m/%d")


def get_link_detail(url, proxy={}, cookie=''):
    headers ={
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
    if proxy:
        ipport = f'{proxy["ip"]}:{proxy["port"]}' if not proxy['username'] else f'{proxy["username"]}:{proxy["password"]}@{proxy["ip"]}:{proxy["port"]}'
        proxy = {
            'http': f'http://{ipport}',
            'https': f'http://{ipport}'
        }
    
    if '/posts/' in url:
        
        response = requests.get(url, headers=headers, proxies=proxy).text
        
        post_id = response.split('"post_id":"')[1].split('"')[0] if '"post_id":"' in response\
            else response.split("'post_id': '")[1].split('\'')[0]
        title = response.split('profile_url')[1].split('"name":"')[1].split('"')[0].encode().decode('unicode_escape')
        content = response.split('"story":{"message":{"text":"')[1].split('"')[1]
        comment_count = response.split('"comments":{"total_count":')[1].split('}')[0]
        created_time = get_publish_time(response)
        return {
            'success': True,
            'data': {
                'post_id': post_id,
                'title': title,
                'content': content,
                'comment_count': comment_count,
                'status': 'public',
                'created_time': created_time,
                'origin_url': url
            }
        }
    
    elif '/reel/' in url:
        response = requests.get(url, headers=headers, proxies=proxy).text
        with open('reel.html', 'w+', encoding='utf-8') as f:
            f.write(response)
        post_id = response.split('"video_id":')[1].split(',')[0]
        title = response.split('"__isActor":"User"')[1].split('"name":"')[1].split('"')[0].encode().decode('unicode_escape')
        content = response.split('"message":{"text":"')[1].split('"')[0]
        comment_count = response.split('"total_comment_count":')[1].split(',')[0]
        created_time = get_publish_time(response)
        return {
            'success': True,
            'data': {
                'post_id': post_id,
                'title': title,
                'content': content,
                'comment_count': comment_count,
                'status': 'public',
                'created_time': created_time,
                'origin_url': url
            }
        }
    
    elif 'story_fbid=' in url:
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

        params = {
            'story_fbid': 'pfbid0vokiMswNuQe8i5GivyvrE59xnFkBRLh8bx65B4xXdzUD8DaRr7YqbFkpUKoaMrjTl',
            'id': '61557549458306',
        }

        response = requests.get('https://www.facebook.com/permalink.php', params=params, headers=headers).text
        # response = requests.get('https://www.facebook.com/permalink.php', headers=headers, params=params).text
        with open('test.html', 'w+', encoding='utf-8') as f:
            f.write(response)
        post_id = response.split('"post_id":"')[1].split('"')[0] if '"post_id":"' in response\
            else response.split("'post_id': '")[1].split('\'')[0]
        title = response.split('profile_url')[1].split('"name":"')[1].split('"')[0].encode().decode('unicode_escape')
        content = response.split('"story":{"message":{"text":"')[1].split('"')[1]
        comment_count = response.split('"comments":{"total_count":')[1].split('}')[0]
        created_time = get_publish_time(response)
        return {
            'success': True,
            'data': {
                'post_id': post_id,
                'title': title,
                'content': content,
                'comment_count': comment_count,
                'status': 'public',
                'created_time': created_time,
                'origin_url': url
            }
        }
        
    else:
        try:
            response = requests.get(url, headers=headers, proxies=proxy).text
            post_id = response.split('"fbid":"')[1].split('"')[0] if '"fbid":"' in response\
                else response.split("'fbid': '")[1].split('\'')[0]
            print(post_id)
            title = response.split('profile_url')[1].split('"name":"')[1].split('"')[0].encode().decode('unicode_escape')
            content = response.split('CometFeedStoryDefaultMessageRenderingStrategy')[1].split('"text":"')[1].split('","delight_ranges"')[0]
            comment_count = response.split('"total_count":')[1].split('}')[0]
            created_time = get_publish_time(response)
            return {
                'success': True,
                'data': {
                    'post_id': post_id,
                    'title': title,
                    'content': content,
                    'comment_count': comment_count,
                    'status': 'public',
                    'created_time': timestamp_to_str(int(created_time)),
                    'origin_url': url
                }
            }
        
        except IndexError:
            headers.update({
                'cookie': cookie
            })
            print(url)
            response = requests.get(url, headers=headers, proxies=proxy).text
            post_id = response.split('"fbid":"')[1].split('"')[0] if '"fbid":"' in response\
                else response.split("'fbid': '")[1].split('\'')[0]
            print(post_id)
            title = response.split('profile_url')[1].split('"name":"')[1].split('"')[0].encode().decode('unicode_escape')
            content = response.split('CometFeedStoryDefaultMessageRenderingStrategy')[1].split('"text":"')[1].split('","delight_ranges"')[0]
            comment_count = response.split('"total_count":')[1].split('}')[0]
            created_time = response.split('"publish_time":')[1].split(',')[0]
            return {
                'success': True,
                'data': {
                    'post_id': post_id,
                    'title': title,
                    'content': content,
                    'comment_count': comment_count,
                    'status': 'public',
                    'created_time': timestamp_to_str(int(created_time)),
                    'origin_url': url
                }
            }
        
        except requests.exceptions.ProxyError:
            return {
                'success': False,
                'data': 'Proxy error'
            }
            
        except Exception as e:
            return {
                'success': False,
                'data': str(e)
            }
