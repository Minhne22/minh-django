from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings
import myproject.settings as settings
import bcrypt
from django.contrib.auth.decorators import login_required
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime
import requests
from datetime import datetime, timezone, timedelta
from .models import Cookie
from .utils import convert_cookie_to_token  # Hàm convert
from .models import Token  # Model lưu tokens
import uuid
import re
from urllib.parse import urlparse, parse_qs, unquote


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

users_collection = settings.users_collection
store_collection = settings.client['store']['admin']
fb_detail = settings.client['fb_cmt_manage']
links_collection = fb_detail['facebook_links']
proxies_collection = fb_detail['proxies']
comments_collection = fb_detail['facebook_comments']

# Function Facebook
def get_link_detail(url, proxy={}, token=''):
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
    if proxy:
        ipport = f'{proxy["ip"]}:{proxy["port"]}' if not proxy['username'] else f'{proxy["username"]}:{proxy["password"]}@{proxy["ip"]}:{proxy["port"]}'
        proxy = {
            'http': f'http://{ipport}',
            'https': f'http://{ipport}'
        }
        session.proxies = proxy
    
    try:
        print(url)
        response = session.get(url).text
        post_id = response.split('"fbid":"')[1].split('"')[0] if '"fbid":"' in response\
            else response.split("'fbid': '")[1].split('\'')[0]
        title = response.split('__isActor')[1].split('"name":"')[1].split('"')[0].encode().decode('unicode_escape')
        content = response.split('CometFeedStoryDefaultMessageRenderingStrategy')[1].split('"text":"')[1].split('"')[0]
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
    
    except IndexError:
        token = store_collection.find_one({"_id": "tokens"})['tokens'][0]
        with open('token_logs.txt', 'a+', encoding='utf8') as f:
            f.write(response + '\n')
        post_id = response.split('"fbid":"')[1].split('"')[0] if '"fbid":"' in response\
            else response.split("'fbid': '")[1].split('\'')[0]
        
        # Get detail using access_token
        response = requests.get(
            f'https://graph.facebook.com/{post_id}',
            params={
                'access_token': token,
                'fields': 'id,from,message,comments.summary(1),created_time'
            }
        ).json()
        
        if 'error' in response:
            error_code = response['error']['code']
            if error_code == 100:
                response = requests.get(
                    f'https://graph.facebook.com/v22.0/{post_id}',
                    params={
                        'access_token': token,
                        'fields': 'id,from.fields(name),description,comments.summary(1),created_time'
                    }
                ).json()
                print(response)
                return {
                    'success': True,
                    'data': {
                        'post_id': post_id,
                        'title': response['from']['name'],
                        'content': response['description'].encode('unicode_escape').decode('utf-8'),
                        'comment_count': response['comments'].get('count', 0),
                        'status': 'private',
                        'created_time': convert_to_utc7(response['created_time']),
                    'origin_url': url
                        
                    }
                }
            else:
                with open('token_logs.txt', 'a+', encoding='utf8') as f:
                    f.write(str(response) + '\n')
        return {
            'success': True,
            'data': {
                'post_id': post_id,
                'title': response['from']['name'],
                'content': response['message'],
                'comment_count': response['comments'].get('count', 0),
                'status': 'private',
                'created_time': convert_to_utc7(response['created_time']),
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

def get_access_token(cookie: str, proxy={}):
    cookie = cookie.split('|')[0]
    app_id = '6628568379'
    cookies = {
       x.split('=')[0]: x.split('=')[1] for x in cookie.replace(' ', '').split(';') if x
    }
    c_user = cookies['c_user']
    headers={
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        # 'cookie': 'locale=en_US; c_user=61551956773750; datr=-Gb2ZgW5OgNTyhK5It1z3fva; sb=-Gb2ZlbohWn-tnP1rUR4VE0y; ps_l=1; ps_n=1; dpr=1.5; fr=1HPw4vTBeTqxiGRaQ.AWUSfAyFMk77kUbM_sKDDypBsTeaZnRyNB_6hg.Bnqfea..AAA.0.0.Bnqfea.AWVQDYLPCcs; xs=31%3A-LSk-cEXXhuvtA%3A2%3A1736995627%3A-1%3A5375%3A%3AAcVxFS7W2AxA78ZYsXbvgxgtGQdVlarwa7ryVEsGKQ; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1739192240120%2C%22v%22%3A1%7D; wd=725x585',
        'dpr': '1.5',
        'priority': 'u=0, i',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-full-version-list': '"Not A(Brand";v="8.0.0.0", "Chromium";v="132.0.6834.160", "Google Chrome";v="132.0.6834.160"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"19.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'viewport-width': '725',
    }
    
    session = requests.Session()
    session.headers.update(headers)
    session.cookies.update(cookies)
    if proxy:
        ipport = f'{proxy["ip"]}:{proxy["port"]}' if not proxy['username'] else f'{proxy["username"]}:{proxy["password"]}@{proxy["ip"]}:{proxy["port"]}'
        proxy = {
            'http': f'http://{ipport}',
            'https': f'http://{ipport}'
        }
        session.proxies = proxy
    
    try:
        # Get fb_dtsg
        response = session.get('https://www.facebook.com/').text
        print(len(response))
        print('Ok')
        with open('fb_dtsg.txt', 'w+', encoding='utf8') as f:
            f.write(response)
        id_user = response.split('"USER_ID":"')[1].split('"')[0] if '"USER_ID":"' in response\
            else response.split("'USER_ID': '")[1].split('\'')[0]
        if id_user == "0":
            return {
                'success': False,
                'data': 'Cookie die'
            }
        fb_dtsg = response.split('{"dtsg":{"token":"')[1].split('"')[0]
        response = session.post('https://www.facebook.com/api/graphql/', data={
            'av': str(c_user),
            '__user': str(c_user),
            'fb_dtsg': fb_dtsg,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'useCometConsentPromptEndOfFlowBatchedMutation',
            'variables': '{"input":{"client_mutation_id":"4","actor_id":"' + c_user + '","config_enum":"GDP_CONFIRM","device_id":null,"experience_id":"' + str(
                uuid.uuid4()
                ) + '","extra_params_json":"{\\"app_id\\":\\"' + app_id + '\\",\\"kid_directed_site\\":\\"false\\",\\"logger_id\\":\\"\\\\\\"' + str(
                uuid.uuid4()
                ) + '\\\\\\"\\",\\"next\\":\\"\\\\\\"confirm\\\\\\"\\",\\"redirect_uri\\":\\"\\\\\\"https:\\\\\\\\\\\\/\\\\\\\\\\\\/www.facebook.com\\\\\\\\\\\\/connect\\\\\\\\\\\\/login_success.html\\\\\\"\\",\\"response_type\\":\\"\\\\\\"token\\\\\\"\\",\\"return_scopes\\":\\"false\\",\\"scope\\":\\"[\\\\\\"user_subscriptions\\\\\\",\\\\\\"user_videos\\\\\\",\\\\\\"user_website\\\\\\",\\\\\\"user_work_history\\\\\\",\\\\\\"friends_about_me\\\\\\",\\\\\\"friends_actions.books\\\\\\",\\\\\\"friends_actions.music\\\\\\",\\\\\\"friends_actions.news\\\\\\",\\\\\\"friends_actions.video\\\\\\",\\\\\\"friends_activities\\\\\\",\\\\\\"friends_birthday\\\\\\",\\\\\\"friends_education_history\\\\\\",\\\\\\"friends_events\\\\\\",\\\\\\"friends_games_activity\\\\\\",\\\\\\"friends_groups\\\\\\",\\\\\\"friends_hometown\\\\\\",\\\\\\"friends_interests\\\\\\",\\\\\\"friends_likes\\\\\\",\\\\\\"friends_location\\\\\\",\\\\\\"friends_notes\\\\\\",\\\\\\"friends_photos\\\\\\",\\\\\\"friends_questions\\\\\\",\\\\\\"friends_relationship_details\\\\\\",\\\\\\"friends_relationships\\\\\\",\\\\\\"friends_religion_politics\\\\\\",\\\\\\"friends_status\\\\\\",\\\\\\"friends_subscriptions\\\\\\",\\\\\\"friends_videos\\\\\\",\\\\\\"friends_website\\\\\\",\\\\\\"friends_work_history\\\\\\",\\\\\\"ads_management\\\\\\",\\\\\\"create_event\\\\\\",\\\\\\"create_note\\\\\\",\\\\\\"export_stream\\\\\\",\\\\\\"friends_online_presence\\\\\\",\\\\\\"manage_friendlists\\\\\\",\\\\\\"manage_notifications\\\\\\",\\\\\\"manage_pages\\\\\\",\\\\\\"photo_upload\\\\\\",\\\\\\"publish_stream\\\\\\",\\\\\\"read_friendlists\\\\\\",\\\\\\"read_insights\\\\\\",\\\\\\"read_mailbox\\\\\\",\\\\\\"read_page_mailboxes\\\\\\",\\\\\\"read_requests\\\\\\",\\\\\\"read_stream\\\\\\",\\\\\\"rsvp_event\\\\\\",\\\\\\"share_item\\\\\\",\\\\\\"sms\\\\\\",\\\\\\"status_update\\\\\\",\\\\\\"user_online_presence\\\\\\",\\\\\\"video_upload\\\\\\",\\\\\\"xmpp_login\\\\\\"]\\",\\"steps\\":\\"{}\\",\\"tp\\":\\"\\\\\\"unspecified\\\\\\"\\",\\"cui_gk\\":\\"\\\\\\"[PASS]:\\\\\\"\\",\\"is_limited_login_shim\\":\\"false\\"}","flow_name":"GDP","flow_step_type":"STANDALONE","outcome":"APPROVED","source":"gdp_delegated","surface":"FACEBOOK_COMET"}}',
            'server_timestamps': 'true',
            'doc_id': '6494107973937368',
        }).json()
        print(response)
        uri = response["data"]["run_post_flow_action"]["uri"]
        print(uri)
        parsed_url = urlparse(uri)

        # Lấy giá trị close_uri từ query string
        query_params = parse_qs(parsed_url.query)
        close_uri = query_params.get("close_uri", [None])[0]

        # Giải mã close_uri để lấy phần chứa access_token
        decoded_close_uri = unquote(close_uri)

        # Phân tích phần fragment của close_uri
        fragment = urlparse(decoded_close_uri).fragment
        fragment_params = parse_qs(fragment)

        # Lấy giá trị access_token
        access_token = fragment_params.get("access_token", [None])[0]
        return {
            'success': True,
            'data': access_token
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



@csrf_exempt
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = users_collection.find_one({"username": username})
        # print(user['password'])
        # print(password)
        # print(generate_password_hash(password))
        if user and check_password_hash(user["password"], password):
            # Lưu session
            request.session["user_id"] = str(user["_id"])
            request.session["username"] = user["username"]
            request.session["role"] = user.get("role", "user")  # Nếu không có role, mặc định là user

            # Trả về JSON để frontend redirect đúng
            return JsonResponse({"status": "success", "role": request.session["role"]}, status=200)
        else:
            return JsonResponse({"status": "error", "message": "Sai tài khoản hoặc mật khẩu"}, status=401)

    return render(request, "accounts/login.html")

def logout_view(request):
    # logout(request)
    request.session.flush()  # Xóa session
    return redirect("login")
@csrf_exempt
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if users_collection.find_one({"username": username}):
            return JsonResponse({"status": "error", "message": "Tài khoản đã tồn tại"}, status=400)

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        users_collection.insert_one({"username": username, "password": hashed_password})

        return JsonResponse({"status": "success", "message": "Đăng ký thành công"}, status=201)

    return JsonResponse({"status": "error", "message": "Phương thức không hợp lệ"}, status=405)

# @login_required
def admin_dashboard(request):
    print("SESSION:", request.session.items())
    if request.session.get("role") != "admin":
        return redirect("login")  # Chỉ admin mới vào được
    return render(request, "accounts/admin_dashboard.html")

# @login_required
def user_dashboard(request):
    if "username" not in request.session:
        return redirect("login")  # Nếu chưa đăng nhập, chuyển về login
    return render(request, "accounts/dashboard.html")

def dashboard_links(request):
    return render(request, "accounts/dashboard_links.html")

def dashboard_comments(request):
    return render(request, "accounts/dashboard_comments.html")

def dashboard_tokens(request):
    return render(request, "accounts/dashboard_tokens.html")

def admin_dashboard(request):
    if request.session.get("role") != "admin":
        return redirect("login")  # Chỉ admin mới truy cập được
    return render(request, "accounts/admin_dashboard.html")

def admin_links(request):
    return render(request, "accounts/admin_links.html")

def admin_comments(request):
    return render(request, "accounts/admin_comments.html")

def admin_tokens(request):
    return render(request, "accounts/admin_tokens.html")

def admin_cookie(request):
    return render(request, "accounts/admin_cookie.html")

def manage_users(request):
    users = list(users_collection.find({}, {"_id": 0}))  # Lấy danh sách user
    return render(request, "accounts/admin_users.html", {"users": users})

def change_role(request, username):
    user = users_collection.find_one({"username": username})
    if not user:
        return JsonResponse({"error": "User không tồn tại"}, status=400)

    new_role = "admin" if user["role"] == "user" else "user"
    users_collection.update_one({"username": username}, {"$set": {"role": new_role}})

    return JsonResponse({"success": True, "new_role": new_role})

def delete_user(request, username):
    result = users_collection.delete_one({"username": username})
    if result.deleted_count == 0:
        return JsonResponse({"error": "User không tồn tại"}, status=400)

    return JsonResponse({"success": True})

def add_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        # Kiểm tra user đã tồn tại chưa
        if users_collection.find_one({"username": username}):
            return JsonResponse({"error": "User đã tồn tại!"}, status=400)

        # Thêm user vào database
        users_collection.insert_one({
            "username": username,
            "password": generate_password_hash(password),
            "role": role
        })

        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request"}, status=400)

def get_links(request):
    """Lấy danh sách link"""
    links = list(links_collection.find({}, {"_id": 0}))
    links = [
        {**link, "content": bytes(link['content'], "utf-8").decode("unicode_escape")}
        for link in links
    ]
    print(links)
    return JsonResponse({"links": links})

@csrf_exempt
def add_links(request):
    if request.method == "POST":
        data = json.loads(request.body)
        links = data.get("links", [])

        inserted_links = []
        for link in links:
            print(link)
            print(link.isnumeric())
            if link.isnumeric():
                link = f'https://facebook.com/{link}'
            print(link)
            
            result = get_link_detail(link)
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
                    'origin_url': result['origin_url']
                }
                # links_collection.insert_one(new_link)
                print(links_collection.update_one(
                    {"post_id": new_link['post_id']},
                    {"$set": new_link}, upsert=True
                ))
                # new_link['_id'] = str(new_link['_id'])
                inserted_links.append(new_link)
        
        print(inserted_links)

        return JsonResponse({"success": True, "links": inserted_links})

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

@csrf_exempt
def edit_link(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get("post_id")
        new_name = data.get("name")
        new_last_comment_time = data.get("last_comment_time")  # Lấy thời gian comment cuối
        new_status = data.get("status")
        new_comment_count = data.get("comment_count")

        if post_id:
            links_collection.update_one(
                {"post_id": post_id},
                {"$set": {
                    "name": new_name,
                    "last_comment_time": new_last_comment_time,  # Cập nhật thời gian comment cuối
                    "status": new_status,
                    "comment_count": int(new_comment_count),
                }}
            )
            return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

@csrf_exempt
def delete_link(request):
    """Xóa link theo post_id"""
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = str(data.get("post_id"))  # Chuyển post_id thành string

        # Kiểm tra nếu link tồn tại
        link = links_collection.find_one({"post_id": post_id})
        if not link:
            return JsonResponse({"success": False, "error": "Link không tồn tại"}, status=400)

        # Xóa link
        links_collection.delete_one({"post_id": post_id})
        return JsonResponse({"success": True})

def admin_proxies(request):
    """Render trang quản lý proxy"""
    return render(request, "accounts/admin_proxies.html")

@csrf_exempt
def get_proxies(request):
    """Lấy danh sách proxy từ MongoDB"""
    proxies = list(proxies_collection.find({}, {"_id": 0}))
    return JsonResponse({"proxies": proxies})

@csrf_exempt
def add_proxy(request):
    """Thêm proxy mới"""
    if request.method == "POST":
        data = json.loads(request.body)
        proxy_input = data.get("proxy")

        parts = proxy_input.split(":")
        if len(parts) not in [2, 4]:  # Chỉ chấp nhận ip:port hoặc ip:port:user:pass
            return JsonResponse({"error": "Định dạng proxy không hợp lệ!"}, status=400)

        proxy_data = {
            "ip": parts[0],
            "port": parts[1],
            "username": parts[2] if len(parts) == 4 else "",
            "password": parts[3] if len(parts) == 4 else "",
            "status": "active"
        }

        # Kiểm tra trùng lặp
        if proxies_collection.find_one({"ip": proxy_data["ip"], "port": proxy_data["port"]}):
            return JsonResponse({"error": "Proxy đã tồn tại!"}, status=400)

        result = proxies_collection.insert_one(proxy_data)
        proxy_data["_id"] = str(result.inserted_id)
        
        return JsonResponse({"success": True, "proxy": proxy_data})

@csrf_exempt
def delete_proxy(request):
    """Xóa proxy"""
    if request.method == "POST":
        data = json.loads(request.body)
        ip, port = data.get("ip"), data.get("port")

        proxies_collection.delete_one({"ip": ip, "port": str(port)})
        return JsonResponse({"success": True})

@csrf_exempt
def toggle_proxy(request):
    """Bật/Tắt proxy"""
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        ip, port = data.get("ip"), data.get("port")

        proxy = proxies_collection.find_one({"ip": ip, "port": str(port)})
        print(proxy)
        if proxy:
            new_status = "inactive" if proxy["status"] == "active" else "active"
            proxies_collection.update_one({"ip": ip, "port": port}, {"$set": {"status": new_status}})
            return JsonResponse({"success": True, "new_status": new_status})

    return JsonResponse({"error": "Proxy không tồn tại"}, status=400)

@csrf_exempt
def add_cookies(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cookies = data.get("cookies", [])

            if not cookies:
                return JsonResponse({"success": False, "message": "Không có dữ liệu!"}, status=400)

            store_collection.update_one(
                {"_id": "cookies"},
                {"$push": {"cookies": {"$each": cookies}}},
                upsert=True
            )

            return JsonResponse({"success": True, "message": "Thêm cookies thành công!"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

def get_cookies(request):
    data = store_collection.find_one({"_id": "cookies"}) or {}
    cookies = data.get("cookies", [])
    return JsonResponse({"success": True, "cookies": cookies})

@csrf_exempt
def delete_cookie(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cookie = data.get("cookie")

            if not cookie:
                return JsonResponse({"success": False, "message": "Cookie không hợp lệ!"}, status=400)

            store_collection.update_one(
                {"_id": "cookies"},
                {"$pull": {"cookies": cookie}}
            )

            return JsonResponse({"success": True, "message": "Xóa cookie thành công!"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

@csrf_exempt
def delete_all_cookies(request):
    store_collection.update_one({"_id": "cookies"}, {"$set": {"cookies": []}})
    return JsonResponse({"success": True, "message": "Đã xóa tất cả cookies!"})


@csrf_exempt
def convert_tokens(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cookies = data.get("cookies", [])

            if not cookies:
                return JsonResponse({"success": False, "message": "Không có dữ liệu!"}, status=400)

            tokens = []
            
            # Chuyển đổi token
            
            for cookie in cookies:
                token = get_access_token(cookie)
                if token:
                    access_token = token['data']
                    tokens.append(access_token)
                

            store_collection.update_one(
                {"_id": "tokens"},
                {"$push": {"tokens": {"$each": tokens}}},
                upsert=True
            )

            return JsonResponse({"success": True, "tokens": tokens})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)


def get_tokens(request):
    data = store_collection.find_one({"_id": "tokens"}) or {}
    tokens = data.get("tokens", [])
    return JsonResponse({"success": True, "tokens": tokens})

@csrf_exempt
def delete_token(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            token = data.get("token")

            if not token:
                return JsonResponse({"success": False, "message": "Token không hợp lệ!"}, status=400)

            store_collection.update_one(
                {"_id": "tokens"},
                {"$pull": {"tokens": token}}
            )

            return JsonResponse({"success": True, "message": "Xóa token thành công!"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

@csrf_exempt
def delete_all_tokens(request):
    store_collection.update_one({"_id": "tokens"}, {"$set": {"tokens": []}})
    return JsonResponse({"success": True, "message": "Đã xóa tất cả tokens!"})

def comment_list(request):
    comments = list(comments_collection.find({}, {"_id": 0}))  # Lấy tất cả comment, không lấy ObjectId
    return JsonResponse({"comments": comments})
