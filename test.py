import requests
import json

ACCESS_TOKEN = "EAAAAAYsX7TsBO2qZBJ9vod7zl2ZA7CfLIg3DjiXZCEKBp0w5iVdUmJEYaM64eqjN8InXCA6dK7GQ3wzmBpwd6WlPT1leyGPUNUoGVj41UHjp5MM6rrbMsYY6xKm8V5XBq6j4AnjAgwzCpuBRFs244NgNnzyNjfePfmHanwlVqXViZAHgGPpJJAZBv8jlm0yXRgwZDZD"
GRAPH_API_URL = "https://graph.facebook.com/v19.0"  # Cập nhật API version phù hợp

# Danh sách yêu cầu batch
batch_data = [
    {"method": "GET", "relative_url": "618458330610133/comments"},
    {"method": "GET", "relative_url": "956251175586540/comments"},
    {"method": "GET", "relative_url": "1290916811896499/comments"},
    {"method": "GET", "relative_url": "503275076031712/comments"},
    # {"method": "GET", "relative_url": "618458330610133/comments"},
    
]

# Gửi request
response = requests.post(
    f"{GRAPH_API_URL}",
    params={"access_token": ACCESS_TOKEN, 'include_headers': 'false'},
    json={"batch": batch_data}
)

# # Xử lý phản hồi
# if response.status_code == 200:
#     responses = response.json()
#     for idx, res in enumerate(responses):
#         print(f"Response {idx + 1}: {json.dumps(res, indent=2)}")
# else:
#     print("Error:", response.text)

# Xử lý phản hồi
print(response.json())
