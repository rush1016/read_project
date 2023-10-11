from django.urls import path
from django.contrib.auth import views as auth_views

from read_app.views import ( 
    home, 
    user_auth, user_register, user_forgot, 
    student_list, student_get_info, section_get_info 
)
from read_app.views.reading import ( 
    add_reading_material, 
    reading_material 
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


    # Student Records Handling
    path('student_list', student_list.student_list, name="student_list"),
    path('get_student_info/<int:student_id>', student_get_info.get_student_info, name="get_student_info"),
    path('get_class_section_data/', section_get_info.get_class_section_data, name="get_class_section_data"),
    # path('add_student', views.add_student, name="add_student"),
    # path('edit_student/<int:student_id>', views.edit_student, name="edit_student"),
    # path('delete_student/<int:student_id>', views.delete_student, name='delete_student'),
    # path('confirm_add_archived_student/<int:archived_student_id>', views.confirm_add_archived_student, name="confirm_add_archived_student"),

    # Reading Materials
    path('reading_material', reading_material.to_reading_materials, name="reading_material"),
    path('add_reading_material', reading_material.to_add_reading_material, name="add_reading_material"),
    path('add_passage', add_reading_material.add_passage, name="add_passage"),
    path('add_question', add_reading_material.add_question, name="add_question"),

]