from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import render, redirect

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            session_lifetime = timedelta(seconds=settings.SESSION_COOKIE_AGE)
            last_activity = request.session.get('last_activity')

            if last_activity:
                last_activity = datetime.fromisoformat(last_activity)
                if datetime.now() - last_activity > session_lifetime:
                    logout(request)  # Kill session
                    request.session.flush()  # Xóa toàn bộ session
                    return redirect('login')  # Chuyển hướng về trang login

            request.session['last_activity'] = datetime.now().isoformat()

        return self.get_response(request)
