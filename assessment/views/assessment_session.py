from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404

from read_app.models import User
from assessment.models import AssessmentSession, AssessmentMiscue
from assessment.forms.assessment_code import AssessmentCodeForm


def student_assessment_list(request):
    student_user_instance = get_object_or_404(User, pk=request.user.id)
    student_instance = student_user_instance.student_instance
    assessment_sessions = AssessmentSession.objects.filter(student=student_instance, is_finished=False)
    context = {
        'assessment_sessions': assessment_sessions,
    }
    return render(request, 'assessment/student/assessment_list.html', context)


def assessment_session_view(request, assessment_id):
    assessment = AssessmentSession.objects.get(pk=assessment_id)
    if assessment.assessment_type == 'Graded':
        assessment_info = assessment.graded_assessment
        assessment_passage = assessment.get_passages()[0]
        passage = assessment_passage.passage
        words = passage.passage_content.split()
        miscues = AssessmentMiscue.objects.filter(passage=passage)
        miscue_words = {miscue.word: miscue.miscue for miscue in miscues}

        context = {
            'words': words,
        }

    context = {
        'passage': passage,
        'assessment': assessment,
        'miscue_words': miscue_words,
        'assessment_info': assessment_info,
    }

    return render(request, 'assessment/assessment_session.html', context)



def assessment_enter_code_view(request):
    if request.method == 'POST':
        form = AssessmentCodeForm(request.POST)
        if form.is_valid():
            passcode = form.cleaned_data['passcode']
            try:
                assessment = AssessmentSession.objects.get(passcode=passcode)
                if assessment.assessment_type == 'Screening':
                    return redirect('screening_assessment', assessment_id=assessment.id, order=assessment.screening_assessment.current_passage)
                elif assessment.assessment_type == 'Graded':
                    return redirect('graded_assessment', assessment_id=assessment.id)

            except:
                messages.error(request, 'Assessment not found. Make sure the passcode is correct.')
                return redirect('assessment_code')

        

    form = AssessmentCodeForm()

    return render(request, 'students/assessment_code.html', {'code_form': form})