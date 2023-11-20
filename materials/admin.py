from django.contrib import admin
from nested_admin import NestedModelAdmin, NestedTabularInline

from materials.forms.PassageAdminForm import PassageAdminForm

from materials.models import (
    AssessmentPreset,
    Passage,
    Question,
    Choice,
)

class PresetAdmin(admin.ModelAdmin):
    list_display = ('grade_level', 'language', 'assessment_type', 'name')



class ChoiceInLine(NestedTabularInline):
    model = Choice
    delete = False
    extra = 0


class QuestionInLine(NestedTabularInline):
    model = Question
    inlines = [ChoiceInLine]
    delete = False
    extra = 0

class PassageAdmin(NestedModelAdmin):
    list_display = ('id', 'preset','set', 'grade_level', 'language', 'passage_title', 'passage_length')
    inlines = [QuestionInLine]

    form = PassageAdminForm


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'passage', 'question_type','question_content', 'created_at')

    inlines = [ChoiceInLine]

    def passage(self, obj):
        return obj.passage.title
    passage.short_description = 'From Passage'


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'choice_content', 'is_correct')

    def question(self, obj):
        return obj.passage.question_content
    

# Passages and Reading Materials
admin.site.register(AssessmentPreset, PresetAdmin)
admin.site.register(Passage, PassageAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)