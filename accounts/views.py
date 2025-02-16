from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse, Http404
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
import time
from markupsafe import escape
import random
from .modules_fb import get_link_detail
from .tasks import get_thong_tin_task
from threading import Thread


def get_timestamp_x_days_later(x):
    today_midnight = datetime.combine(datetime.today(), datetime.min.time())  # 0h hôm nay
    target_date = today_midnight + timedelta(days=x)  # Cộng thêm X ngày
    return int(target_date.timestamp())

def check_live_cookie(cookie: str, proxy=''):
    for _ in range(5):
        ipport = f'{proxy["ip"]}:{proxy["port"]}' if not proxy['username'] else f'{proxy["username"]}:{proxy["password"]}@{proxy["ip"]}:{proxy["port"]}'
        
        print(ipport)
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'priority': 'u=0, i',
            'cookie': cookie,
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
        
        session = requests.Session()
        session.headers.update(headers)
        session.proxies = {'http': f'http://{ipport}', 'https': f'http://{ipport}'}  # Sử dụng proxy
        try:
            response = session.get('https://www.facebook.com/').text
            fb_dtsg = response.split('["DTSGInitialData",[],{"token":"')[1].split('"')[0]
            print(fb_dtsg)
            name = response.split('"NAME":"')[1].split('"')[0].encode().decode('unicode_escape')
            user_id = response.split('"USER_ID":"')[1].split('"')[0]
            return {
                'status': 'active',
                'name': name,
                'user_id': user_id,
            }
        
        except (requests.exceptions.ConnectionError, 
            requests.exceptions.Timeout, 
            requests.exceptions.RequestException) as e:
            pass
        
        except IndexError:
            return {
                'status': 'die'
            }
        
        except Exception as e:
            print(e)
            return {
                'status': 'die'
            }
    else:
        return {
            'status': 'proxy_die',
            'proxy_data': proxy
        }
    
users_collection = settings.users_collection

fb_detail = settings.client['fb_cmt_manage']
links_collection = fb_detail['facebook_links']
proxies_collection = fb_detail['proxies']
comments_collection = fb_detail['facebook_comments']

store_credentials = settings.client['store']
cookie_collection = store_credentials['cookies']
token_collection = store_credentials['tokens']

# User Database Link
users_db = settings.client['user_links']

# User Database Cookie
users_cookie_db = settings.client['user_cookies']

# User Database Comments
user_comments_collection = settings.client['user_comments']

# Function Facebook

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
            date = user.get('days_remaining', 0)
            print(date)
            if date == 0 or date < int(time.time()):
                return JsonResponse({"status": "error", "message": "Hết hạn sử dụng"})
            # Lưu session
            request.session["user_id"] = str(user["_id"])
            request.session["username"] = user["username"]
            request.session["role"] = user.get("role", "user")  # Nếu không có role, mặc định là user
            request.session.set_expiry(date)
            today_midnight = datetime.combine(datetime.today(), datetime.min.time())  # 0h hôm nay
            request.session['days_remaining'] = (datetime.fromtimestamp(date)  - today_midnight).days

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
# def admin_dashboard(request):
#     print("SESSION:", request.session.items())
#     today_midnight = datetime.combine(datetime.today(), datetime.min.time())  # 0h hôm nay
#     user = users_collection.find_one({"username": request.session.get("username")})
#     request.session['days_remaining'] = (datetime.fromtimestamp((user.get('days_remaining', time.time()))  - today_midnight)).days
#     print(request.session['days_remaining'])
#     if request.session.get("role") != "admin":
#         return redirect("login")  # Chỉ admin mới vào được
#     return render(request, "accounts/admin_dashboard.html")

# @login_required
def user_dashboard(request):
    if "username" not in request.session:
        return redirect("login")  # Nếu chưa đăng nhập, chuyển về login
    user = users_collection.find_one({"username": request.session.get("username")})
    date = user.get('days_remaining', 0)
    today_midnight = datetime.combine(datetime.today(), datetime.min.time())  # 0h hôm nay
    request.session['days_remaining'] = (datetime.fromtimestamp(date)  - today_midnight).days
    return render(request, "accounts/dashboard.html")

def dashboard_links_on(request):
    return render(request, "accounts/dashboard_links.html")

def dashboard_links_off(request):
    return render(request, "accounts/dashboard_links_off.html")

def dashboard_comments(request):
    return render(request, "accounts/dashboard_comments.html")

def dashboard_cookie(request):
    return render(request, "accounts/dashboard_cookie.html")

def admin_dashboard(request):
    if not request.session.get("username"):
        return redirect("login") 
    if request.session.get("role") != "admin":
        raise Http404("Page not found")
    today_midnight = datetime.combine(datetime.today(), datetime.min.time())  # 0h hôm nay
    user = users_collection.find_one({"username": request.session.get("username")})
    request.session['days_remaining'] = (datetime.fromtimestamp((user.get('days_remaining', time.time()))) - today_midnight).days
    print(request.session['days_remaining'])
    if request.session.get("role") != "admin":
        return redirect("login")  # Chỉ admin mới truy cập được
    return render(request, "accounts/admin_dashboard.html")

# def admin_links(request):
#     return render(request, "accounts/admin_links.html")

def admin_links_on(request):
    return render(request, "accounts/admin_links.html")

def admin_links_off(request):
    return render(request, "accounts/admin_links_off.html")

def admin_comments(request):
    return render(request, "accounts/admin_comments.html")

def admin_tokens(request):
    return render(request, "accounts/admin_tokens.html")

def admin_cookie(request):
    return render(request, "accounts/admin_cookie.html")

def manage_users(request):
    if not request.session.get('role') == 'admin':
        return JsonResponse({"error": "Bạn không có quyền truy cập"}, status=403)
    users = list(users_collection.find({}, {"_id": 0}))  # Lấy danh sách user
    today_midnight = datetime.combine(datetime.today(), datetime.min.time())  # 0h hôm nay
    users = [
        {**user, "days_remaining": (datetime.fromtimestamp(user.get('days_remaining', time.time()))  - today_midnight).days} for user in users
    ]
    # days_difference = (today_midnight - datetime.fromtimestamp(users.get('days_remaining', 0))).days  # Tính số ngày
    return render(request, "accounts/admin_users.html", {"users": users})

def change_role(request, username):
    user = users_collection.find_one({"username": username})
    if not user:
        return JsonResponse({"error": "User không tồn tại"}, status=400)

    new_role = "admin" if user["role"] == "user" else "user"
    users_collection.update_one({"username": username}, {"$set": {"role": new_role}})

    return JsonResponse({"success": True, "new_role": new_role})

@csrf_exempt
def edit_limit(request, username):
    if request.method == "POST":
        user = users_collection.find_one({"username": username})
        if not user:
            return JsonResponse({"error": "User không tồn tại"}, status=400)

        limit_on = request.POST.get("limit_on")
        limit_off = request.POST.get("limit_off")
        days_remaining = request.POST.get("days_remaining")
        

        if not limit_on or not limit_off or not days_remaining:
            return JsonResponse({"error": "Thiếu thông tin cần thiết"}, status=400)

        users_collection.update_one(
            {"username": username},
            {"$set": {"limit_on": int(limit_on), "limit_off": int(limit_off), "days_remaining": get_timestamp_x_days_later(int(days_remaining))}}
        )

        return JsonResponse({"success": True, "limit_on": limit_on, "limit_off": limit_off, "days_remaining": days_remaining})

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def change_pass(request, username):
    if request.method == "POST":
        user = users_collection.find_one({"username": username})
        if not user:
            return JsonResponse({"error": "User không tồn tại"}, status=400)

        new_password = request.POST.get("password")
        if not new_password:
            return JsonResponse({"error": "Thiếu mật khẩu mới"}, status=400)

        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        users_collection.update_one(
            {"username": username},
            {"$set": {"password": hashed_password}}
        )

        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request"}, status=400)
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

def get_links_on(request):
    """Lấy danh sách link"""
    if request.session.get("role") == "admin":
        links = list(links_collection.find({"active": "on"}, {"_id": 0}))
        links = [
            {**link, "content": escape(link.get('content', '').encode().decode('unicode_escape'))} for link in links
        ][::-1]
        # print(links)
        return JsonResponse({"links": links})
    else:
        username = request.session.get("username")
        user_links_collection = users_db[username]
        links = list(user_links_collection.find({}, {"_id": 0}))
        links = [
            {**link, "content": escape(link.get('content', '').encode().decode('unicode_escape'))} for link in links
        ][::-1]
        return JsonResponse({"links": links})
        

def get_links_off(request):
    """Lấy danh sách link"""
    links = list(links_collection.find({}, {"_id": 0, "active": "off"}))
    links = [
        {**link, "content": link['content'].encode().decode('unicode_escape')} for link in links
    ][::-1]
    # print(links)
    return JsonResponse({"links": links})

@csrf_exempt
def add_links(request):
    if request.method == "POST":
        if request.session.get("role") == "admin":
            data = json.loads(request.body)
            links = data.get("links", [])
            username = request.session.get("username")
            user = users_collection.find_one({"username": username}, {"_id": 0})
            limit_on = user.get("limit_on", 0)
            links_available = links_collection.count_documents({"active": "on"})
            if (links_available + len(links)) > limit_on:
                return JsonResponse({"success": False, "error": "Vượt quá giới hạn link"}, status=400)
            
            
            for link in links:
                if link.isnumeric():
                    link = f'https://facebook.com/{link}'
                proxy = random.choice(list(proxies_collection.find({"status": "active"})))
                # print(proxy)
                cookie = random.choice(list(cookie_collection.find({"status": "active"})))['cookie']
                # print(cookie)
                
                links_collection.insert_one({"origin_url": link, "status": "pending"})
                Thread(target=get_thong_tin_task, args=(links_collection, link, cookie, proxy, )).start()

            return JsonResponse({"message": "URLs đã được thêm và đang xử lý"}, status=200)
        else:
            username = request.session.get("username")
            user_links_collection = users_db[username]
            data = json.loads(request.body)
            links = data.get("links", [])
            user = users_collection.find_one({"username": username}, {"_id": 0})
            limit_on = user.get("limit_on", 0)
            links_available = user_links_collection.count_documents({})
            if (links_available + len(links)) > limit_on:
                return JsonResponse({"success": False, "error": "Vượt quá giới hạn link"}, status=400)
            for link in links:
                if link.isnumeric():
                    link = f'https://facebook.com/{link}'
                proxy = random.choice(list(proxies_collection.find({"status": "active"})))
                # print(proxy)
                cookie = random.choice(list(cookie_collection.find({"status": "active"})))['cookie']
                # print(cookie)
                
                links_collection.insert_one({"origin_url": link, "status": "pending"})
                Thread(target=get_thong_tin_task, args=(links_collection, link, cookie, proxy, )).start()
                
            return JsonResponse({"message": "URLs đã được thêm và đang xử lý"}, status=200)


    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

@csrf_exempt
def edit_link(request):
    if request.method == "POST":
        if request.session.get("role") == "admin":
            data = json.loads(request.body)
            post_id = data.get("post_id")
            new_name = data.get("name")
            new_status = data.get("status")
            delay = data.get("delay")
            delay = int(delay) if delay else 5

            if post_id:
                links_collection.update_one(
                    {"post_id": post_id},
                    {"$set": {
                        "name": new_name,
                        "status": new_status,
                        "delay": delay
                    }}
                )
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "error": "Không tìm thấy link"}, status=400)
        else:
            username = request.session.get("username")
            user_links_collection = users_db[username]
            data = json.loads(request.body)
            post_id = data.get("post_id")
            new_name = data.get("name")
            new_content = data.get("content")
            
            if post_id:
                user_links_collection.update_one(
                    {"post_id": post_id},
                    {"$set": {
                        "name": new_name,
                        "content": new_content
                    }}
                )
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "error": "Không tìm thấy link"}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

@csrf_exempt
def delete_link(request):
    """Xóa link theo post_id"""
    if request.method == "POST":
        if request.session.get("role") == "admin":
            data = json.loads(request.body)
            post_id = str(data.get("post_id"))  # Chuyển post_id thành string

            # Kiểm tra nếu link tồn tại
            link = links_collection.find_one({"post_id": post_id})
            if not link:
                return JsonResponse({"success": False, "error": "Link không tồn tại"}, status=400)

            # Xóa link
            links_collection.delete_one({"post_id": post_id})
            return JsonResponse({"success": True})
        else:
            username = request.session.get("username")
            user_links_collection = users_db[username]
            data = json.loads(request.body)
            post_id = str(data.get("post_id"))
            link = user_links_collection.find_one({"post_id": post_id})
            if not link:
                return JsonResponse({"success": False, "error": "Link không tồn tại"}, status=400)
            user_links_collection.delete_one({"post_id": post_id})
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
            print(new_status)
            proxies_collection.update_one({"ip": ip, "port": str(port)}, {"$set": {"status": new_status}})
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
            
            proxies = list(proxies_collection.find({"status": "active"}))  # Lấy danh sách proxy đang hoạt động

            for cookie in cookies:
                print(cookie)
                
                while True:
                    proxy = random.choice(proxies) if proxies else {}
                    status = check_live_cookie(cookie, proxy)
                    if status['status'] == 'proxy_die':
                        proxies_collection.update_one(
                            {"ip": proxy['ip'], "port": str(proxy['port'])},
                            {"$set": {"status": "inactive"}}
                        )
                    else:
                        break
                cookie_collection.update_one(
                    {"cookie": cookie},
                    {"$set": {"cookie": cookie, **status}},
                    upsert=True
                )

            return JsonResponse({"success": True, "message": "Thêm cookies thành công!"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

def get_cookies(request):
    if request.session.get("role") == "admin":
        data = list(cookie_collection.find({}, {"_id": 0}))
        print(data)
        return JsonResponse({"success": True, "cookies": data})
    else:
        username = request.session.get("username")
        user_cookies_collection = users_db[username]
        data = list(user_cookies_collection.find({}, {"_id": 0}))
        return JsonResponse({"success": True, "cookies": data})

    

@csrf_exempt
def delete_cookie(request):
    if request.method == "POST":
        if request.session.get("role") == "admin":
            try:
                data = json.loads(request.body)
                cookie = data.get("cookie")

                if not cookie:
                    return JsonResponse({"success": False, "message": "Cookie không hợp lệ!"}, status=400)

                cookie_collection.delete_one({"cookie": cookie})

                return JsonResponse({"success": True, "message": "Xóa cookie thành công!"})
            except Exception as e:
                return JsonResponse({"success": False, "message": str(e)}, status=500)
        else:
            username = request.session.get("username")
            user_cookies_collection = users_db[username]
            data = json.loads(request.body)
            cookie = data.get("cookie")
            if not cookie:
                return JsonResponse({"success": False, "message": "Cookie không hợp lệ!"}, status=400)
            user_cookies_collection.delete_one({"cookie": cookie})
            return JsonResponse({"success": True, "message": "Xóa cookie thành công!"})

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

@csrf_exempt
def delete_all_cookies(request):
    if request.session.get("role") == "admin":
        cookie_collection.delete_many({})
        return JsonResponse({"success": True, "message": "Đã xóa tất cả cookies!"})
    else:
        username = request.session.get("username")
        user_cookies_collection = users_db[username]
        user_cookies_collection.delete_many({})
        return JsonResponse({"success": True, "message": "Đã xóa tất cả cookies!"})


@csrf_exempt
def convert_tokens(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cookies = data.get("cookies", [])

            if not cookies:
                return JsonResponse({"success": False, "message": "Không có dữ liệu!"}, status=400)

            successes = []
            
            # Chuyển đổi token
            
            for cookie in cookies:
                token = get_access_token(cookie)
                if token:
                    access_token = token['data']
                    successes.append({"cookie": cookie, "token": access_token, "status": "active"})
                

            token_collection.insert_many(successes)
            successes = [
                {**success, "_id": str(success['_id'])} for success in successes
            ]

            return JsonResponse({"success": True, "tokens": successes})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)


def get_tokens(request):
    tokens = list(token_collection.find({}, {"_id": 0}))
    return JsonResponse({"success": True, "tokens": tokens})

@csrf_exempt
def delete_token(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            token = data.get("token")

            if not token:
                return JsonResponse({"success": False, "message": "Token không hợp lệ!"}, status=400)

            token_collection.delete_one({"token": token})

            return JsonResponse({"success": True, "message": "Xóa token thành công!"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

@csrf_exempt
def delete_all_tokens(request):
    token_collection.delete_many({})
    return JsonResponse({"success": True, "message": "Đã xóa tất cả tokens!"})

def comment_list(request):
    if request.session.get("role") == "admin":
        start_time = request.GET.get("start_date")
        start_time = datetime.strptime(start_time, "%d-%m-%Y")
        start_time = datetime(start_time.year, start_time.month, start_time.day, 0, 0, 0).timestamp()
        end_time = request.GET.get("end_date")
        end_time = datetime.strptime(end_time, "%d-%m-%Y")
        end_time = datetime(end_time.year, end_time.month, end_time.day, 23, 59, 59).timestamp()
        print(start_time, end_time)
        query = {"time": {"$gte": start_time, "$lt": end_time}}    
        comments = list(comments_collection.find(query, {"_id": 0}).sort('time', -1))  # Lấy tất cả comment, không lấy ObjectId
        return JsonResponse({"comments": comments})
    else:
        username = request.session.get("username")
        user_comments_collection = users_db[username]
        start_time = request.GET.get("start_date")
        start_time = datetime.strptime(start_time, "%d-%m-%Y")
        start_time = datetime(start_time.year, start_time.month, start_time.day, 0, 0, 0).timestamp()
        end_time = request.GET.get("end_date")
        end_time = datetime.strptime(end_time, "%d-%m-%Y")
        end_time = datetime(end_time.year, end_time.month, end_time.day, 23, 59, 59).timestamp()
        query = {"time": {"$gte": start_time, "$lt": end_time}}
        comments = list(user_comments_collection.find(query, {"_id": 0}).sort('time', -1))
        return JsonResponse({"comments": comments})

def get_user_limit(request):
    username = request.session.get("username")
    user = users_collection.find_one({"username": username}, {"_id": 0})
    limit_on = user.get("limit_on", 0)
    user['limit_on'] = limit_on 
    return JsonResponse({'limit_on': limit_on})