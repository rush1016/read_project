from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from read_app.models import (
    User, 
    Admin,
    Teacher, 
    School,
    Grade,
    ClassSection,
)

class UserAdmin(UserAdmin):
    list_display = (
        'id', 
        'username', 
        'first_name', 
        'last_name', 
        'email', 
        'is_teacher', 
        'is_school_admin'
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_school_admin', 'is_teacher')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'is_school_admin')
        }),
    ) 


class AdministratorAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'first_name', 'last_name', 'date_created')
    # Define methods to access User model fields
    def first_name(self, obj):
        return obj.user.first_name
    first_name.short_description = 'First Name'

    def last_name(self, obj):
        return obj.user.last_name
    last_name.short_description = 'Last Name'


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


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('school_code', 'registration_code', 'name', 'district', 'division', 'region')
    filter = ('grade_level')


class GradeAdmin(admin.ModelAdmin):
    list_display = ('grade_level', 'grade_name')
    filter = ('grade_level')


class ClassSectionAdmin(admin.ModelAdmin):
    list_display = ('grade_level', 'section_name')
    filter = ('grade_level')
    search_field = ('section_name')

# User accounts
admin.site.register(User, UserAdmin)
admin.site.register(Admin, AdministratorAdmin)
admin.site.register(Teacher, TeacherAdmin)


admin.site.register(School, SchoolAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(ClassSection, ClassSectionAdmin)