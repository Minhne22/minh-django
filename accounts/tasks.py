import requests
import time
from pymongo import MongoClient
from .modules_fb import Get_Link_Detail


def get_thong_tin_task(collection, url, cookie, proxy={}):
    MAX_RETRIES = 5
    collection.update_one({"origin_url": url}, {"$set": {"active": "pending"}}, upsert=True)
    for _ in range(MAX_RETRIES):
        try:
            client = Get_Link_Detail(url, proxy)
            try:
                result = client.get_all()
                result['data']['status'] = 'public'
                
            except IndexError as e:
                with open("log-task.txt", "a+") as f:
                    f.write(f"{e} - Retrying {url}...\n")
                result = client.get_all(cookie=cookie)
                result['data']['status'] = 'private'
            
            # print(result)
            
            if result['success']:
                result = result['data']
                new_link = {
                    "post_id": result['post_id'],
                    "created_time": result['created_time'],
                    "name": result['title'],
                    "last_comment_time": 'Proccessing',
                    "comment_count": result['comment_count'],
                    "status": result['status'],
                    "content": result['content'],
                    'origin_url': result['origin_url'],
                    'active': 'on',
                    'delay': 5,
                    'encoded_post': result['encoded_post']
                }
                collection.update_one(
                    {"origin_url": new_link['origin_url']},
                    {"$set": new_link}
                )
                print('Ok')
            return 'Done'
        except Exception as e:
            error = e
            with open("log-task.txt", "a+") as f:
                f.write(f"{e} - Retrying {url}...\n")
            time.sleep(2)
            
    else:
        collection.update_one({"origin_url": url}, {"$set": {"active": "failed", "error": str(error)}})
