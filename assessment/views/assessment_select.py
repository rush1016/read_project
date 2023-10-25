from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib import messages
from django.db import transaction

from read_app.models import User
from students.models import Student
from materials.models import Passage, AssessmentPreset
from assessment.models import AssessmentSession, AssessmentSessionPassage
from assessment.forms.preset_select import PresetSelect

def select(request):
    return render(request, 'assessment/assessment_select.html')

def select_student_screening(request):
    teacher_instance = User.objects.get(pk=request.user.id, is_teacher=True)
    students = Student.objects.filter(
        teacher=teacher_instance, 
        assessments_done=0, 
        is_screened = False,
        is_approved=True,
        screening=False,
    ).order_by('student_id')

    form = PresetSelect()

    context = {
        'students': students,
        'assessment_type': 'Screening',
        'form': form,
    }
    return render(request, 'assessment/assessment_student_select.html', context)


def select_material_graded(request):
    passages = Passage.objects.filter(preset=None)
    teacher_instance = User.objects.get(pk=request.user.id, is_teacher=True)
    students = Student.objects.filter(
        teacher=teacher_instance, 
        is_approved=True
    ).order_by('student_id')

    context = {
        'passages': passages,
        'students': students,
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
        grade_level=passage_instance.grade_level
        ).order_by('student_id')

    context = {
        'mode': 'select student',
        'students': students,
        'passage': passage_instance,
    }

    return render(request, 'assessment/assessment_student_select.html', context)


@transaction.atomic
def assign_assessment(request, assessment_type):
    if request.method == 'POST':
        student_list = request.POST.getlist('selected_records')

        for student in student_list:
            student_user_instance = get_object_or_404(User, pk=student)
            student_instance = get_object_or_404(Student, user=student_user_instance)
            assessment_session = AssessmentSession.objects.create(
                student = student_instance,
                assessment_type = assessment_type,
                grade_level = student_instance.grade_level,
            )

            if assessment_type == 'Screening':
                preset_id = request.POST.get('preset_select')
                assign_screening(assessment_session, preset_id)
                student_instance.save()
        
            elif assessment_type == 'Graded':
                passage_id = request.POST.get('passage_id')
                assign_graded(assessment_session, passage_id)

            assessment_session.save()
            messages.success(request, 'Successfully assigned assessment.')
         
    return redirect('assessment_select')


def assign_screening(assessment_session, preset_id):
    preset = get_object_or_404(AssessmentPreset, pk=preset_id)
    passages = get_list_or_404(Passage, preset=preset)
            
    for passage in passages:
        AssessmentSessionPassage.objects.create(
            assessment_session = assessment_session,
            passage = passage,
        )

def assign_graded(assessment_session, passage_id):
    passage_instance = get_object_or_404(Passage, pk=passage_id)
    AssessmentSessionPassage.objects.create(
        assessment_session = assessment_session,
        passage = passage_instance,
    )