from django.urls import path
from . import views

# Add urls here
urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_user, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('register', views.register_user, name="register"),
    path('forgot', views.toForgotPage, name="forgot"),
    path('otp', views.toOtpPage, name="otp")
]