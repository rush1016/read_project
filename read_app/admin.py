from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from read_app.models import User, Teacher, Student, ClassSection, Passage, Question, Choice

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
    list_display = ('user', 'first_name', 'last_name', 'teacher_code', 'email', 'date_created')

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


class ClassSectionAdmin(admin.ModelAdmin):
    list_display = ('grade_level', 'section_name')
    filter = ('grade_level')
    search_field = ('section_name')


class PassageAdmin(admin.ModelAdmin):
    list_display = ('id', 'grade_level', 'passage_title', 'passage_content')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'passage', 'question_content', 'created_at')

    def passage(self, obj):
        return obj.passage.title
    passage.short_description = 'From Passage'


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'choice_content', 'is_correct')

    def question(self, obj):
        return obj.passage.question_content


# User accounts
admin.site.register(User, UserAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)

# Passages and Reading Materials
admin.site.register(Passage, PassageAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)


"""admin.site.register(ArchivedStudent, ArchivedStudentAdmin) """
admin.site.register(ClassSection, ClassSectionAdmin)