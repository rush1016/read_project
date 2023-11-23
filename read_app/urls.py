from django.urls import path
from django.contrib.auth import views as auth_views

from read_app.views import ( 
    home, 
)
from read_app.views.user import (
    user_auth, user_register, user_forgot, 
)
from read_app.forms.custom_password_confirm_form import CustomPasswordResetConfirmForm

from read_app.views.user import profile, change_email, change_password
from read_app.views.reports import generate_report, generate_srp_report
from read_app.views.admin import teacher_list
from read_app.views.admin import class_view


# Add urls here
urlpatterns = [
    path('', home.home, name='home'),

    # Account handling
    path('login', user_auth.login_user, name="login"),
    path('logout', user_auth.logout_user, name="logout"),
    

    # User Registration
    path('register', user_register.register, name="register"),
    path('register/teacher', user_register.teacher_register, name="teacher_register"),

    # Password Reset
    path('forgot', user_forgot.forgot_password_request, name="forgot"),
    path('password_reset', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(form_class=CustomPasswordResetConfirmForm), name='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Generate Report
    path('report/isr/<int:student_id>', generate_report.download_report, name="generate_report"),
    path('report/srp/<int:school_id>', generate_srp_report.generate_srp_report_view, name="generate_srp"),

    # Teacher profile
    path('profile', profile.teacher_profile_view, name="teacher_profile"),
    path('profile/email/change', change_email.change_email_view, name="change_email"),
    path('profile/password/change', change_password.change_password_view, name="change_password"),

    # Admin Controls
    path('list/teacher/<int:school_id>', teacher_list.teacher_list_view, name="teacher_list"),
    path('view/class/<int:teacher_user_id>', class_view.class_view, name="view_class"),
]