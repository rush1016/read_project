from django.contrib import admin
from students.models import (
    Student, 
    ClassSection, 
    ArchivedStudent,
)


class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'user', 
        'student_school_id', 
        'last_name', 
        'first_name', 
        'teacher', 
        'grade_level', 
        'class_section', 
        'date_added', 
        'is_approved',
        'screening',
        'is_screened',
    )

    # Define methods to access User model fields
    def first_name(self, obj):
        return obj.user.first_name
    first_name.short_description = 'First Name'

    def last_name(self, obj):
        return obj.user.last_name
    last_name.short_description = 'Last Name'

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


class ClassSectionAdmin(admin.ModelAdmin):
    list_display = ('grade_level', 'section_name')
    filter = ('grade_level')
    search_field = ('section_name')


admin.site.register(Student, StudentAdmin)
admin.site.register(ArchivedStudent, ArchivedStudentAdmin)

admin.site.register(ClassSection, ClassSectionAdmin)