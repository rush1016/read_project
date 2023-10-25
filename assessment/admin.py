from django.contrib import admin

from assessment.forms.student_answer_admin import StudentAnswerAdminForm
from assessment.models import (
    AssessmentSession,
    AssessmentSessionPassage,
    StudentAnswer,
)

class AssessmentSessionAdmin(admin.ModelAdmin):
    list_display = (
        'student', 
        'assessment_type', 
        'grade_level', 
        'total_score', 
        'total_reading_time', 
        'total_answering_time',
        'assigned_time',
        'start_time',
        'end_time',
        'is_finished',
    )

class AssessmentPassageAdmin(admin.ModelAdmin):
    list_display = (
        'assessment_session',
        'order',
        'passage',
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
admin.site.register(StudentAnswer, StudentAnswerAdmin)