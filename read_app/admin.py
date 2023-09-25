from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Teacher, Student

# Teacher (User)
class TeacherAdmin(UserAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'date_created', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'date_created')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'date_created'),
        }),
    )

admin.site.register(Teacher, TeacherAdmin)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'first_name', 'last_name', 'grade_level', 'date_added')
    list_filter = ('grade_level', 'date_added')
    search_fields = ('first_name', 'last_name')
    ordering = ('date_added',)

admin.site.register(Student, StudentAdmin)