from django.contrib import admin
from students.models import (
    Student,
    StudentRating,
    ArchivedStudent,
)


class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'school',
        'last_name', 
        'first_name', 
        'teacher', 
        'grade_level', 
        'recommended_grade_level',
        'class_section', 
        'date_added', 
        'screening',
        'is_screened',
        'overall_rating',
        'assessments_done',
    )

    # Define methods to access User model fields
    def first_name(self, obj):
        return obj.user.first_name
    first_name.short_description = 'First Name'

    def last_name(self, obj):
        return obj.user.last_name
    last_name.short_description = 'Last Name'

class StudentRatingAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'english_rating',
        'english_recommended_grade',
        'filipino_rating',
        'filipino_recommended_grade',
    )

class ArchivedStudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id',
        'student_school_id',
        'previous_teacher', 
        'first_name', 
        'last_name', 
        'grade_level', 
        'class_section', 
        'date_added', 
        'is_approved', 
        'date_archived'
    )




admin.site.register(Student, StudentAdmin)
admin.site.register(StudentRating, StudentRatingAdmin)
admin.site.register(ArchivedStudent, ArchivedStudentAdmin)
