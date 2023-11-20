from django.urls import path

from assessment.views import (
    assessment_select,
    assessment_assign,
    assessment_session,
    assessment_result,
    assessment_info,
    assessment_adaptive_assign,
    miscue,
    gst_score,
)
from assessment.views.calculations import (
    reading_level,
)

from assessment.views.assessment_types import (
    screening_test,
    graded_assessment_session,
)

urlpatterns = [
    # Miscues
    path('miscue/save', miscue.save_miscue_view, name="save_miscue"),
    path('miscue/delete', miscue.delete_miscue_view, name="delete_miscue"),
    path("miscue/get", miscue.get_miscue_view , name="get_miscue"),


    # Calculations
    path("score/level/<int:assessment_id>", reading_level.calculate_reading_level_view, name="calculate_reading_level"),
    path("gst/score/add/<int:student_id>", gst_score.add_gst_score, name="add_gst"),

    # Select
    path('select', assessment_select.select, name="assessment_select"),
    path('enter_code', assessment_session.assessment_enter_code_view, name="assessment_code"),

    path('screening/select_student', assessment_select.select_student_screening, name="select_student_screening"),
    path('graded/select', assessment_select.select_material_graded, name="select_material_graded"),
    path('graded/select/students', assessment_select.select_student_graded, name="select_student_graded"),

    path('list', assessment_info.assessment_list_view, name="assessment_list"),
    path('view/<int:assessment_id>', assessment_info.assessment_info_view, name="assessment_info"),

    path('assign/<str:assessment_type>', assessment_assign.assign_assessment, name="assign_assessment"),
    path('my_assessments', assessment_session.student_assessment_list, name="student_assessment_list"),

    path('recommended/<int:student_id>', assessment_adaptive_assign.assign_recommended_view, name="assign_recommended"),


    # Session
    path('session/<int:assessment_id>', assessment_session.assessment_session_view, name="assessment_session"),

    path('screening/<int:assessment_id>/<int:order>', screening_test.screening_assessment_view, name="screening_assessment"),
    path('screening/next/<int:assessment_id>/<int:order>', screening_test.screening_save_answers_view, name="screening_assessment_next"),

    path('graded/<int:assessment_id>', graded_assessment_session.graded_assessment_view, name="graded_assessment"),


    # Results
    path('result/<int:assessment_id>', assessment_result.assessment_result_view, name="assessment_done" ),

    # View info
    path('view/<int:assessment_id>', assessment_info.assessment_info_view, name="view_assessment") 
]