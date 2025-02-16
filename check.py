import requests
import urllib.parse

link = 'https://www.facebook.com/tranthimyduyendang'
link = link.encode().decode('unicode_escape')
link = urllib.parse.unquote(link)

headers = {
    'authority': 'www.facebook.com',
    'accept': '*/*',
    'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'cache-control': 'no-cache',
    'cookie': 'datr=DcuxZ59JzOfc7qIVO6wDNJvC; dpr=1.5; sb=EMuxZwc0tQ4x7uV9if3L9mmi; ar_debug=1; wd=842x551',
    'content-type': 'application/x-www-form-urlencoded',
    'dnt': '1',
    'origin': 'https://www.facebook.com',
    'pragma': 'no-cache',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'x-fb-lsd': 'AVod3gKj3Nk',
}

data = {
    "client_previous_actor_id": "",
    "route_url": link,
    "routing_namespace": "fb_comet",
    "__aaid": "0",
    "__user": "0",
    "__a": "1",
    "__req": "12",
    "dpr": "1",
    "__ccg": "GOOD",
    "__comet_req": "15",
    "lsd": 'AVod3gKj3Nk',
    "jazoest": '2933',
    "__spin_b": "trunk",
}

response_url_user = requests.post(
    'https://www.facebook.com/ajax/navigation/', 
    headers=headers,
    data=data).text
with open('check.json', 'w+') as f:
    f.write(response_url_user)