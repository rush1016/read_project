from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomPasswordResetConfirmForm


# Add urls here
urlpatterns = [
    path('', views.home, name='home'),

    # Account handling
    path('login', views.login_user, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('register', views.register_user, name="register"),
    path('forgot', views.forgot_password_request, name="forgot"),

    # Password Reset
    path('password_reset', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(form_class=CustomPasswordResetConfirmForm), name='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Student Records Handling
    path('student_list', views.student_list, name="student_list"),
    path('add_student', views.add_student, name="add_student"),
    path('get_student_info/<int:student_id>', views.get_student_info, name="get_student_info"),
    path('edit_student/<int:student_id>', views.edit_student, name="edit_student"),
    path('delete_student/<int:student_id>', views.delete_student, name='delete_student'),
    path('get_class_section_data/', views.get_class_section_data, name="get_class_section_data"),
    path('confirm_add_archived_student/<int:archived_student_id>', views.confirm_add_archived_student, name="confirm_add_archived_student"),
]