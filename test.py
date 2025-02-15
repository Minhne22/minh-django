# import requests
# import json

# ACCESS_TOKEN = "EAAAAAYsX7TsBO2qZBJ9vod7zl2ZA7CfLIg3DjiXZCEKBp0w5iVdUmJEYaM64eqjN8InXCA6dK7GQ3wzmBpwd6WlPT1leyGPUNUoGVj41UHjp5MM6rrbMsYY6xKm8V5XBq6j4AnjAgwzCpuBRFs244NgNnzyNjfePfmHanwlVqXViZAHgGPpJJAZBv8jlm0yXRgwZDZD"
# GRAPH_API_URL = "https://graph.facebook.com/v19.0"  # Cập nhật API version phù hợp

# # Danh sách yêu cầu batch
# batch_data = [
#     {"method": "GET", "relative_url": "618458330610133/comments"},
#     {"method": "GET", "relative_url": "956251175586540/comments"},
#     {"method": "GET", "relative_url": "1290916811896499/comments"},
#     {"method": "GET", "relative_url": "503275076031712/comments"},
#     # {"method": "GET", "relative_url": "618458330610133/comments"},
    
# ]

# # Gửi request
# response = requests.post(
#     f"{GRAPH_API_URL}",
#     params={"access_token": ACCESS_TOKEN, 'include_headers': 'false'},
#     json={"batch": batch_data}
# )

# # # Xử lý phản hồi
# # if response.status_code == 200:
# #     responses = response.json()
# #     for idx, res in enumerate(responses):
# #         print(f"Response {idx + 1}: {json.dumps(res, indent=2)}")
# # else:
# #     print("Error:", response.text)

# # Xử lý phản hồi
# print(response.json())



import requests

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

response = requests.get('https://www.facebook.com/permalink.php', params=params, headers=headers)

with open('fbuid.html', 'w+', encoding='utf-8') as f:
    f.write(response.text)