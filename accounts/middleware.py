from django.shortcuts import redirect
from django.conf import settings

def admin_required(get_response):
    def middleware(request):
        if request.session.get("role") != "admin":
            return redirect("login")  # Chặn nếu không phải admin
        return get_response(request)
    return middleware
