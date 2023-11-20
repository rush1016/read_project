from django.urls import path

from students.views import (
    student_profile,
    student_list, 
    student_get_info, 
    section_get_info, 
    add_student,
    approve_student,
    student_edit_view,
    student_delete_view
)

urlpatterns = [
    # Student Records Handling
    path('list', student_list.student_list, name="student_list"),
    path('student/<int:student_id>', student_profile.student_profile_view, name="student_profile"),
    path('get_student_info/<int:student_id>', student_get_info.get_student_info, name="get_student_info"),
    path('get_class_section_data/', section_get_info.get_class_section_data, name="get_class_section_data"),

    path('add', add_student.add_student, name="add_student"),
    path('approve/<int:student_id>', approve_student.approve_student, name="approve_student"),
    path('edit/<int:student_id>', student_edit_view.student_edit, name="edit_student"),
    path('delete/<int:student_id>', student_delete_view.student_delete, name='delete_student'),

    # Check existing records
    path('check_existing_student', add_student.check_existing_student, name="check_existing_student")
]