from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Teacher, Student, ArchivedStudent, ClassSection

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


class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher_id', 'first_name', 'last_name', 'grade_level', 'class_section','date_added')
    list_filter = ('grade_level', 'class_section','date_added')
    search_fields = ('first_name', 'last_name')
    ordering = ('date_added',)


class ArchivedStudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher_id', 'first_name', 'last_name', 'grade_level', 'class_section','date_archived')
    list_filter = ('grade_level', 'class_section','date_archived')
    search_fields = ('first_name', 'last_name')
    ordering = ('date_archived',)


class ClassSectionAdmin(admin.ModelAdmin):
    list_display = ('grade_level', 'section_name')
    filter = ('grade_level')
    search_field = ('section_name')


# Register Models into the Admin Site
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(ArchivedStudent, ArchivedStudentAdmin)
admin.site.register(ClassSection, ClassSectionAdmin)