from django.urls import path
from django.contrib.auth import views as auth_views

from read_app.views import ( 
    home, 
)
from read_app.views.user import (
    user_auth, user_register, user_forgot, 
)
from read_app.forms.custom_password_confirm_form import CustomPasswordResetConfirmForm

from read_app.views.user import (
    profile, 
    change_email, 
    change_password, 
    change_username
)

from read_app.views.reports import (
    individual_summary_report, 
    school_summary_report, 
    class_summary_report
)
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
    path('report/isr/<int:student_id>', individual_summary_report.generate_report, name="generate_individual"),
    path('report/srp/<int:school_id>', school_summary_report.generate_report, name="generate_school"),
    path('report/csr/<int:teacher_id>', class_summary_report.generate_report, name="generate_class"),

    # Teacher profile
    path('profile', profile.teacher_profile_view, name="teacher_profile"),
    path('profile/change/email', change_email.change_email_view, name="change_email"),
    path('profile/change/username', change_username.change_username_view, name="change_username"),
    path('profile/change/password', change_password.change_password_view, name="change_password"),

    # Admin Controls
    path('list/teacher/<int:school_id>', teacher_list.teacher_list_view, name="teacher_list"),
    path('view/class/<int:teacher_user_id>', class_view.class_view, name="view_class"),
]