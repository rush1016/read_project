from django.urls import path

from students.views import (
    student,
    student_list, 
    student_get_info, 
    section_get_info, 
    approve_student,
    student_edit_view,
    student_delete_view
)

urlpatterns = [
    # Student Records Handling
    path('list', student_list.student_list, name="student_list"),
    path('student/<int:student_id>', student.student_profile_view, name="student_profile"),
    path('get_student_info/<int:student_id>', student_get_info.get_student_info, name="get_student_info"),
    path('get_class_section_data/', section_get_info.get_class_section_data, name="get_class_section_data"),
    path('approve/<int:student_id>', approve_student.approve_student, name="approve_student"),
    path('edit/<int:student_id>', student_edit_view.student_edit, name="edit_student"),
    path('delete/<int:student_id>', student_delete_view.student_delete, name='delete_student'),
]