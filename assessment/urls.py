from django.urls import path

from assessment.views import (
    assessment_select,
    assessment_assign,
    assessment_session,
    assessment_result,
    assessment_info,
    screening_test,
    graded_assessment_session,
)

urlpatterns = [
    # Select
    path('select', assessment_select.select, name="assessment_select"),
    path('screening/select_student', assessment_select.select_student_screening, name="select_student_screening"),
    path('graded/select', assessment_select.select_material_graded, name="select_material_graded"),
    path('graded/select/students', assessment_select.select_student_graded, name="select_student_graded"),

    path('list', assessment_info.assessment_list_view, name="assessment_list"),
    path('view/<int:assessment_id>', assessment_info.assessment_info_view, name="assessment_info"),

    path('assign/<str:assessment_type>', assessment_assign.assign_assessment, name="assign_assessment"),
    path('my_assessments', assessment_session.student_assessment_list, name="student_assessment_list"),

    # Session
    path('screening/<int:assessment_id>/<int:order>', screening_test.screening_assessment_view, name="screening_assessment"),
    path('screening/next/<int:assessment_id>/<int:order>', screening_test.screening_save_answers_view, name="screening_assessment_next"),

    path('graded/<int:assessment_id>', graded_assessment_session.graded_assessment_view, name="graded_assessment"),

    # Results
    path('result/<int:assessment_id>', assessment_result.assessment_result_view, name="assessment_done" ),

    # View info
    path('view/<int:assessment_id>', assessment_info.assessment_info_view, name="view_assessment") 
]