import requests
def get_link_detail(url, proxy={}, credential={}):
    session = requests.Session()
    session.headers.update({
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
        'viewport-width': '819'})
    
    # try:
    response = session.get(url).text
    with open('check.html', 'w+', encoding='utf8') as f:
        f.write(response)
    post_id = response.split('"fbid":"')[1].split('"')[0] if '"fbid":"' in response\
        else response.split("'fbid': '")[1].split('\'')[0]
    title = response.split('profile_url')[1].split('"name":"')[1].split('"')[0].encode().decode('unicode_escape')
    content = response.split('CometFeedStoryDefaultMessageRenderingStrategy')[1].split('"text":"')[1].split('"')[0]
    content = bytes(content, "utf-8").decode("unicode_escape", "surrogatepass")
    print(len(content))
    print(post_id)
    print(title)
    # print(content)
    
    return {
        'post_id': post_id,
        'title': title,
        'content': content
    }
        
    # except:
    #     return 'cc'
    

res = get_link_detail('https://www.facebook.com/61566434843797/videos/1940734799759031/#')
print(res)