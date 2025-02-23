import requests

encoded_posts = 'ZmVlZGJhY2s6MTIyMTIxODAyMTAwNjkyMDcx'

headers = {
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
    'variables': '{"commentsIntentToken":"RECENT_ACTIVITY_INTENT_V1","feedLocation":"DEDICATED_COMMENTING_SURFACE","feedbackSource":110,"focusCommentID":null,"scale":1,"useDefaultActor":false,"id":"' + encoded_posts + '","__relay_internal__pv__IsWorkUserrelayprovider":false}',
    'server_timestamps': 'true',
    'doc_id': '9051058151623566',
}

response = requests.post('https://www.facebook.com/api/graphql/', headers=headers, data=data).text
with open('hi.json', 'w+') as f:
    f.write(response)