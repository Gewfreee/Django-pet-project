from django.urls import path
from . import views


urlpatterns = [
    path('signup', views.SignUpView, name='signup'),
    path('login', views.LogInView, name='login'),
    path('logout', views.LogOutView, name='logout'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
]