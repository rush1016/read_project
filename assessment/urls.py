from django.urls import path

from assessment.views import (
    assessment_select,
    assessment_session,
    assessment_list,
)

urlpatterns = [
    # Select
    path('select', assessment_select.select, name="assessment_select"),
    path('screening/select_student', assessment_select.select_student_screening, name="select_student_screening"),
    path('graded/select', assessment_select.select_material_graded, name="select_material_graded"),
    path('graded/select/students', assessment_select.select_student_graded, name="select_student_graded"),

    path('list', assessment_list.assessment_list_view, name="assessment_list"),

    path('assign/<str:assessment_type>', assessment_select.assign_assessment, name="assign_assessment"),
    path('student/list', assessment_session.student_assessment_list, name="student_assessment_list"),

    # Session
    path('screening/<int:assessment_id>', assessment_session.screening_assessment_start, name="screening_assessment"),
    path('graded/<int:assessment_id>', assessment_session.assessment_view, name="graded_assessment"),
    path('done/<int:assessment_id>', assessment_session.assessment_result_view, name="assessment_done" )

]