from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from read_app.models import (
    User, 
    Teacher, 
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


# User accounts
admin.site.register(User, UserAdmin)
admin.site.register(Teacher, TeacherAdmin)