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
from accounts.views import login_view, logout_view, register_view, admin_dashboard, user_dashboard, admin_comments, admin_links, admin_tokens, dashboard_comments, dashboard_links, dashboard_tokens, manage_users, delete_user, change_role, add_user


urlpatterns = [
    path('', user_dashboard, name='home'),
    path('admin/', admin.site.urls),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
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
]
