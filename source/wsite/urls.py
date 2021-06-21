from django.contrib import admin
from django.contrib import admin
from django.contrib import admin
from django.urls import path
from wsite import views

urlpatterns = [
    path('', views.dashboard, name = 'Dashboard'),
    path('about', views.about, name = 'About'),
    path('login', views.login, name = 'Login'),

    path('ac-admin/password-change', views.adminPassUpdate, name = 'UpdateAdminPass'),
 
    path('accounts/new', views.userCreate, name = 'CreateUser'),
    path('accounts/update/<int:id>/', views.userUpdate, name = 'UpdateUser'),
    path('accounts/all', views.usersAll, name = 'AllUsers'),
    path('accounts/active', views.usersAct, name = 'ActiveUsers'),
    path('accounts/inactive', views.usersDct, name = 'InactiveUsers'),
    path('accounts/suspended', views.usersSus, name = 'SuspendedUsers'),
 

    path('accounts/lock/<int:id>/', views.userLock, name = 'LockUser'),
    path('accounts/unlock/<int:id>/', views.userUnlock, name = 'UnlockUser'),
    path('accounts/suspend/<int:id>/', views.userSuspend, name = 'SuspendUser'),
    path('accounts/activate/<int:id>/', views.userActivate, name = 'ActivateUser'),
    path('accounts/search', views.userSearch, name = 'SearchUser'),
 


]