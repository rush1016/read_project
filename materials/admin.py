from django.contrib import admin

from materials.models import (
    AssessmentPreset,
    Passage,
    Question,
    Choice,
)

class PresetAdmin(admin.ModelAdmin):
    list_display = ('grade_level', 'assessment_type', 'name')

class PassageAdmin(admin.ModelAdmin):
    list_display = ('id', 'preset','grade_level', 'passage_title', 'passage_content', 'passage_length')


class ChoiceInLine(admin.TabularInline):
    model = Choice


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'passage', 'question_content', 'created_at')

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