from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('fasting/start/', views.start_fasting_view, name='start_fasting'),
    path('fasting/end/', views.end_fasting_view, name='end_fasting'),
    path('fasting/history/', views.history_view, name='history'),
    path('fasting/edit/<int:pk>/', views.edit_fasting_view, name='edit_fasting'),
    path('weight/', views.weight_view, name='weight'),
]
