from django.contrib import admin
from django.contrib import admin
from django.contrib import admin
from django.urls import path
from wsite import views

urlpatterns = [
    path('', views.dashboard, name = 'dashboard'),
    path('about', views.about, name = 'about'),
    path('login', views.adminLogin, name = 'login'),
    path('logout', views.adminLogout, name = 'logout'),

    path('ac-admin/password-change', views.adminPassUpdate, name = 'update_admin_pass'),
 
    path('accounts/new', views.userCreate, name = 'create_user'),
    path('accounts/update/<int:id>/', views.userUpdate, name = 'update_user'),
    path('accounts/all', views.usersAll, name = 'all_users'),
    path('accounts/active', views.usersAct, name = 'active_users'),
    path('accounts/inactive', views.usersDct, name = 'inactive_users'),
    path('accounts/suspended', views.usersSus, name = 'suspended_users'),
 

    path('accounts/lock/<int:id>/', views.userLock, name = 'lock_user'),
    path('accounts/unlock/<int:id>/', views.userUnlock, name = 'unlock_user'),
    path('accounts/suspend/<int:id>/', views.userSuspend, name = 'suspend_user'),
    path('accounts/activate/<int:id>/', views.userActivate, name = 'activate_user'),
    path('accounts/search', views.userSearch, name = 'search_user'),
 


]