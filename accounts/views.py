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

users_collection = settings.users_collection
fb_detail = settings.client['fb_cmt_manage']
links_collection = fb_detail['facebook_links']
proxies_collection = fb_detail['proxies']

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
    return JsonResponse({"links": links})

@csrf_exempt
def add_link(request):
    """Thêm link mới (Lấy thông tin từ backend)"""
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get("post_id")

        # Giả lập dữ liệu lấy từ backend
        new_link = {
            "time_created": datetime.now().strftime("%H:%M:%S %Y/%m/%d"),
            "post_id": post_id,
            "post_name": f"Tiêu đề bài {post_id}",
            "content": f"Nội dung bài {post_id}",
            "last_comment_time": "10h",
            "comment_count": 100,
            "like_count": 500,
            "delay": "300ms",
        }
        
        result = links_collection.update_one(
            {"post_id": post_id},
            {"$set": new_link}
        )
        new_link["_id"] = str(result.inserted_id)
        return JsonResponse({"success": True, "link": new_link})

@csrf_exempt
def edit_link(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get("post_id")
        new_name = data.get("name")
        new_last_comment_time = data.get("last_comment_time")  # Lấy thời gian comment cuối
        new_status = data.get("status")
        new_comment_count = data.get("comment_count")
        new_like_count = data.get("like_count")
        new_delay = data.get("delay")

        if post_id:
            links_collection.update_one(
                {"post_id": post_id},
                {"$set": {
                    "name": new_name,
                    "last_comment_time": new_last_comment_time,  # Cập nhật thời gian comment cuối
                    "status": new_status,
                    "comment_count": int(new_comment_count),
                    "like_count": int(new_like_count),
                    "delay": new_delay
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
