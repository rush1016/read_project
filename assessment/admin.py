from django.contrib import admin

from assessment.forms.student_answer_admin import StudentAnswerAdminForm
from assessment.models import (
    AssessmentSession,
    AssessmentSessionPassage,
    ScreeningAssessment,
    GradedAssessment,
    StudentAnswer,
)

class AssessmentSessionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'student', 
        'assessment_type', 
        'grade_level',
        'number_of_questions',
        'total_score', 
        'total_reading_time', 
        'total_answering_time',
        'assigned_time',
        'start_time',
        'end_time',
        'is_finished',
    )


class ScreeningAssessmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'assessment_session',
        'current_passage',
        'correct_literal',
        'correct_inferential',
        'correct_critical',
        'total_literal',
        'total_inferential',
        'total_critical',
    )

class AssessmentPassageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'assessment_session',
        'order',
        'passage',
        'score',
        'reading_time',
        'answering_time',
    )

class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'assessment',
        'student',
        'passage',
        'question',
        'answer',
        'correct',
    )
    form = StudentAnswerAdminForm


# Assessments
admin.site.register(AssessmentSession, AssessmentSessionAdmin)
admin.site.register(AssessmentSessionPassage, AssessmentPassageAdmin)
admin.site.register(ScreeningAssessment, ScreeningAssessmentAdmin)
admin.site.register(GradedAssessment)

admin.site.register(StudentAnswer, StudentAnswerAdmin)