from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Teacher, Student, ClassSection

# Teacher (User)
class UserAdmin(UserAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'is_student', 'is_teacher', 'is_school_admin')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')
        }),
    ) 

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'date_created')

    # Define methods to access User model fields
    def first_name(self, obj):
        return obj.user.first_name
    first_name.short_description = 'First Name'

    def last_name(self, obj):
        return obj.user.last_name
    last_name.short_description = 'Last Name'

    def email(self, obj):
        return obj.user.email
    email.short_description = 'Email'


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_name', 'first_name', 'teacher', 'grade_level', 'class_section', 'date_added', 'is_approved')

    # Define methods to access User model fields
    def first_name(self, obj):
        return obj.user.first_name
    first_name.short_description = 'First Name'

    def last_name(self, obj):
        return obj.user.last_name
    last_name.short_description = 'Last Name'




""" class ArchivedStudentAdmin(admin.ModelAdmin):
    list_filter = ('grade_level', 'class_section','date_archived')
    search_fields = ('first_name', 'last_name')
    ordering = ('date_archived',) """


class ClassSectionAdmin(admin.ModelAdmin):
    list_display = ('grade_level', 'section_name')
    filter = ('grade_level')
    search_field = ('section_name')


# Register Models into the Admin Site
admin.site.register(User, UserAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
"""admin.site.register(ArchivedStudent, ArchivedStudentAdmin) """
admin.site.register(ClassSection, ClassSectionAdmin)