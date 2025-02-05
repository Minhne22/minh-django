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

users_collection = settings.users_collection


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = users_collection.find_one({"username": username})
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
