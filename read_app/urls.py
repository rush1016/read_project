from django.urls import path
from . import views

# Add urls here
urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.toLoginPage, name="login"),
    path('register', views.toRegisterPage, name="register"),
    path('forgot', views.toForgotPage, name="forgot"),
]