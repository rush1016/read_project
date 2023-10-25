from django.urls import path
from django.contrib.auth import views as auth_views

from read_app.views import ( 
    home, 
)
from read_app.views.user import (
    user_auth, user_register, user_forgot, 
)
from read_app.forms.custom_password_confirm_form import CustomPasswordResetConfirmForm


# Add urls here
urlpatterns = [
    path('', home.home, name='home'),

    # Account handling
    path('login', user_auth.login_user, name="login"),
    path('logout', user_auth.logout_user, name="logout"),
    

    # User Registration
    path('register', user_register.registration, name="register"),
    path('register/student', user_register.student_registration, name='student_registration'),
    path('register/teacher', user_register.teacher_registration, name="teacher_registration"),


    # Password Reset
    path('forgot', user_forgot.forgot_password_request, name="forgot"),
    path('password_reset', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(form_class=CustomPasswordResetConfirmForm), name='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]