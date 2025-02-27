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
from accounts.views import admin_dashboard, user_dashboard, admin_comments, admin_links_on, admin_links_off, admin_tokens, dashboard_comments, dashboard_links_on, dashboard_links_off, dashboard_cookie, admin_cookie
from accounts.views import login_view, logout_view, register_view, manage_users, delete_user, change_role, add_user, \
    get_links_on, get_links_off, delete_link, add_links, add_links_off, edit_link, \
        admin_proxies, get_proxies, add_proxy, delete_proxy, toggle_proxy, \
            edit_limit, change_pass, toggle_link_active
from accounts.views import add_cookies, get_cookies, delete_cookie, delete_all_cookies
from accounts.views import convert_tokens, get_tokens, delete_token, delete_all_tokens
from accounts.views import comment_list, get_user_limit
from accounts.views import file_upload, show_data, admin_phone

urlpatterns = [
    path('', user_dashboard, name='home'),
    path('admin/', admin.site.urls),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("admin-dashboard/cookie/", admin_cookie, name="admin_cookie"),
    path("admin-dashboard/links-on/", admin_links_on, name="admin_links_on"),
    path("admin-dashboard/links-off/", admin_links_off, name="admin_links_off"),
    path("admin-dashboard/comments/", admin_comments, name="admin_comments"),
    path("admin-dashboard/tokens/", admin_tokens, name="admin_tokens"),
    path("admin-dashboard/phone/", admin_phone, name="admin_phone"),
    path("dashboard/", user_dashboard, name="user_dashboard"),
    path("dashboard/links-on/", dashboard_links_on, name="dashboard_links"),
    path("dashboard/links-off/", dashboard_links_off, name="dashboard_links_off"),
    path("dashboard/comments/", dashboard_comments, name="dashboard_comments"),
    path("dashboard/cookie/", dashboard_cookie, name="dashboard_cookied"),
    path("admin-dashboard/users/", manage_users, name="manage_users"),
    path("admin-dashboard/delete-user/<str:username>/", delete_user, name="delete_user"),
    path("admin-dashboard/change-role/<str:username>/", change_role, name="change_role"),
    path("admin-dashboard/edit-limit/<str:username>/", edit_limit, name="edit_limit"),
    path("admin-dashboard/change-pass/<str:username>/", change_pass, name="change_pass"),
    path("admin-dashboard/add-user/", add_user, name="add_user"),
    path("api/get_links_on/", get_links_on, name="get_links_on"),
    path("api/get_links_off/", get_links_off, name="get_links_off"),
    path("api/delete_link/", delete_link, name="delete_link"),
    path("api/add_links/", add_links, name="add_links"),
    path("api/add_links_off/", add_links, name="add_links_off"),
    path("admin-dashboard/proxies/", admin_proxies, name="admin_proxies"),
    path("api/api/get_proxies/", get_proxies, name="get_proxies"),
    path("api/api/add_proxy/", add_proxy, name="add_proxy"),
    path("api/api/delete_proxy/", delete_proxy, name="delete_proxy"),
    path("api/api/toggle_proxy/", toggle_proxy, name="toggle_proxy"),
    path("api/api/edit_link/", edit_link, name="edit_link"),
    path("api/api/add_cookies/", add_cookies, name="add_cookies"),
    path("api/api/get_cookies/", get_cookies, name="get_cookies"),
    path("api/api/delete_cookie/", delete_cookie, name="delete_cookie"),
    path("api/api/convert_tokens/", convert_tokens, name="convert_tokens"),
    path("api/api/get_tokens/", get_tokens, name="get_tokens"),
    path("api/api/delete_token/", delete_token, name="delete_token"),
    path("api/api/delete_all_tokens/", delete_all_tokens, name="delete_all_tokens"),
    path("api/api/delete_all_cookies/", delete_all_cookies, name="delete_all_cookies"),
    path("api/api/comment_list/", comment_list, name="comment_list"),
    path("api/api/get_user_limit/", get_user_limit, name="get_user_limit"),
    path("api/api/toggle_link_active/", toggle_link_active, name="toggle-active"),
    path('api/upload/', file_upload, name='file_upload'),
    path('api/show_data/',show_data, name='show_data'),
    # path("convert-cookie/", convert_cookie_to_token, name="convert_cookie_to_token"),
]
