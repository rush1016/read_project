from django.urls import path
from django.contrib.auth import views as auth_views

from read_app.views import ( 
    home, 
)
from read_app.views.user import (
    user_auth, user_register, user_forgot, 
)
from read_app.views.students import (
    student_list, 
    student_get_info, 
    section_get_info, 
    approve_student,
    student_edit_view,
    student_delete_view
)
from read_app.views.reading import ( 
    add_reading_material, 
    reading_material,
    get_passage_info,
    delete_reading_material,
    manage_passage
)
from read_app.views.assessment import (
    assessment_select,
    assessment_session
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
    path('approve_student/<int:student_id>', approve_student.approve_student, name="approve_student"),
    path('edit_student/<int:student_id>', student_edit_view.student_edit, name="edit_student"),
    path('delete_student/<int:student_id>', student_delete_view.student_delete, name='delete_student'),


    # Reading Materials
    path('reading_material', reading_material.to_reading_materials, name="reading_material"),
    path('add_reading_material', add_reading_material.add_reading_material, name="add_reading_material"),
    path('manage_passage/<int:passage_id>', manage_passage.manage_passage, name="manage_passage"),
    path('delete_passage/<int:passage_id>', delete_reading_material.delete_passage, name="delete_passage"),
    path('get_passage_info/<int:passage_id>', get_passage_info.get_passage_info, name="get_passage_info"),


    # Assessments
    path('assessment/select', assessment_select.select, name="assessment/select"),
    path('assessment/screening/select_student', assessment_select.select_student_screening, name="assessment/screening/select_student"),
    path('assessment/assign', assessment_select.assign_screening_assessment, name="assessment/assign"),

    path('assessment/list', assessment_session.student_assessment_list, name="assessment/list"),
]