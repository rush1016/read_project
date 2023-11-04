from django.shortcuts import render, get_object_or_404, get_list_or_404

from read_app.models import User
from students.models import Student
from materials.models import Passage, AssessmentPreset
from assessment.models import AssessmentSession
from assessment.forms.preset_select import PresetSelect

def select(request):
    return render(request, 'assessment/assessment_select.html')

def select_student_screening(request):
    teacher_instance = User.objects.get(pk=request.user.id, is_teacher=True)
    students = Student.objects.filter(
        teacher=teacher_instance, 
        assessments_done=0, 
        is_approved=True,
    ).order_by('student_id')

    form = PresetSelect()

    context = {
        'students': students,
        'assessment_type': 'Screening',
        'form': form,
    }
    return render(request, 'assessment/assessment_student_select.html', context)


def select_material_graded(request):
    graded_presets = [
        'Grade 4 Graded Passage', 
        'Grade 5 Graded Passage', 
        'Grade 6 Graded Passage'
        ]
    preset_instances = get_list_or_404(AssessmentPreset, name__in=graded_presets)
    passages = Passage.objects.filter(preset__in=preset_instances)

    context = {
        'passages': passages,
        'assessment_type': 'Graded',
    }

    return render(request, 'assessment/assessment_student_select.html', context)


def select_student_graded(request):
    passage_id = request.GET.get('passageId')
    passage_instance = get_object_or_404(Passage, pk=passage_id)
    teacher_instance = get_object_or_404(User, pk=request.user.id, is_teacher=True)


    students = Student.objects.filter(
        teacher=teacher_instance, 
        is_approved=True,
        is_screened=True,
        grade_level=passage_instance.grade_level,
    ).order_by('student_id')

    context = {
        'mode': 'select student',
        'students': students,
        'passage': passage_instance,
    }

    return render(request, 'assessment/assessment_student_select.html', context)