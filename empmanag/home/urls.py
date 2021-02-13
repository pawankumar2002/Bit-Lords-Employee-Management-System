from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/<int:emp_id>/', views.dashboard, name='dashboard'),
    path('attandance/<int:emp_id>/', views.attandance, name='attandance'),
    path('update/<int:emp_id>/', views.update, name='update'),
]


admin.site.site_header = 'Employee Management Administration'