"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts.views import admin_dashboard, user_dashboard, admin_comments, admin_links, admin_tokens, dashboard_comments, dashboard_links, dashboard_tokens, admin_cookie
from accounts.views import login_view, logout_view, register_view, manage_users, delete_user, change_role, add_user, \
    get_links, delete_link, add_links, edit_link, \
        admin_proxies, get_proxies, add_proxy, delete_proxy, toggle_proxy
from accounts.views import add_cookies, get_cookies, delete_cookie, delete_all_cookies
from accounts.views import convert_tokens, get_tokens, delete_token, convert_cookie_to_token, delete_all_tokens
from accounts.views import comment_list, comment_page

urlpatterns = [
    path('', user_dashboard, name='home'),
    path('admin/', admin.site.urls),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("admin-dashboard/cookie/", admin_cookie, name="admin_cookie"),
    path("admin-dashboard/links/", admin_links, name="admin_links"),
    path("admin-dashboard/comments/", admin_comments, name="admin_comments"),
    path("admin-dashboard/tokens/", admin_tokens, name="admin_tokens"),
    path("dashboard/", user_dashboard, name="user_dashboard"),
    path("dashboard/links/", dashboard_links, name="dashboard_links"),
    path("dashboard/comments/", dashboard_comments, name="dashboard_comments"),
    path("dashboard/tokens/", dashboard_tokens, name="dashboard_tokens"),
    path("admin-dashboard/users/", manage_users, name="manage_users"),
    path("admin-dashboard/delete-user/<str:username>/", delete_user, name="delete_user"),
    path("admin-dashboard/change-role/<str:username>/", change_role, name="change_role"),
    path("admin-dashboard/add-user/", add_user, name="add_user"),
    path("admin-dashboard/get_links/", get_links, name="get_links"),
    path("admin-dashboard/delete_link/", delete_link, name="delete_link"),
    path("admin-dashboard/add_links/", add_links, name="add_links"),
    path("admin-dashboard/proxies/", admin_proxies, name="admin_proxies"),
    path("admin-dashboard/api/get_proxies/", get_proxies, name="get_proxies"),
    path("admin-dashboard/api/add_proxy/", add_proxy, name="add_proxy"),
    path("admin-dashboard/api/delete_proxy/", delete_proxy, name="delete_proxy"),
    path("admin-dashboard/api/toggle_proxy/", toggle_proxy, name="toggle_proxy"),
    path("admin-dashboard/api/edit_link/", edit_link, name="edit_link"),
    path("admin-dashboard/api/add_cookies/", add_cookies, name="add_cookies"),
    path("admin-dashboard/api/get_cookies/", get_cookies, name="get_cookies"),
    path("admin-dashboard/api/delete_cookie/", delete_cookie, name="delete_cookie"),
    path("admin-dashboard/api/convert_tokens/", convert_tokens, name="convert_tokens"),
    path("admin-dashboard/api/get_tokens/", get_tokens, name="get_tokens"),
    path("admin-dashboard/api/delete_token/", delete_token, name="delete_token"),
    path("admin-dashboard/api/delete_all_tokens/", delete_all_tokens, name="delete_all_tokens"),
    path("admin-dashboard/api/delete_all_cookies/", delete_all_cookies, name="delete_all_cookies"),
    path("admin-dashboard/api/comment_list/", comment_list, name="comment_list"),
    path("admin-dashboard/api/comment_page/", comment_page, name="comment_page"),
    # path("convert-cookie/", convert_cookie_to_token, name="convert_cookie_to_token"),
]
