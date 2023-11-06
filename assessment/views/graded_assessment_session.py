from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from django.db import models

from read_app.models import User
from materials.models import Passage, Choice
from assessment.models import AssessmentSession, AssessmentSessionPassage, StudentAnswer
from assessment.views.check_answer import check_answer
from assessment.views.update_passage_data import update_assessment_passage_data
from assessment.views.calculate_overall_rating import calculate_overall_rating

from assessment.forms.question import AssessmentQuestionForm


@transaction.atomic
def graded_assessment_view(request, assessment_id):
    assessment_instance = get_object_or_404(AssessmentSession, pk=assessment_id)
    assessment_passages = assessment_instance.get_passages()
    student_user_instance = get_object_or_404(User, pk=request.user.id)
    student_instance = student_user_instance.student_instance
    
    # Set the start_time to when the user first clicked the begin button
    if assessment_instance.start_time == None:
        assessment_instance.start_time = start_time = timezone.now()
        assessment_instance.save()
    else:
        start_time = assessment_instance.start_time

    # Check if assessment is already finished
    if assessment_instance.is_finished == True:
        messages.error(request, 'Assessment already finished.')
        return redirect('student_assessment_list')

    # Check if the assessment is valid Graded Passages Assessment
    if len(assessment_instance.get_passages()) > 1:
        messages.error(request, 'Invalid assessment')
        return redirect('assessment_list')

    # Get the content from the database
    passage_instance = assessment_passages[0].passage
    questions = passage_instance.get_questions()
    
    # Generate the question forms for the assessment
    question_forms = [AssessmentQuestionForm(question=question) for question in questions]

    if request.method == 'POST':
        passage_id = request.POST.get('passage_id')
        reading_time = request.POST.get('reading_time')
        answering_time = request.POST.get('answering_time')
        score = 0

        for question in questions:
            answer_field_name = f'answer_content_{question.id}'
            answer_id = request.POST.get(answer_field_name)
            choice_instance = get_object_or_404(Choice, pk=answer_id)
            correct = False

            if check_answer(question, choice_instance):
                score += 1
                correct = True
            # Saving progress
            StudentAnswer.objects.get_or_create(
                assessment=assessment_instance,
                student=student_instance,
                passage=passage_instance,
                question=question,
                answer=choice_instance,
                correct=correct
            )

        # AssessmentSessionPassage model
        update_assessment_passage_data(passage_id, assessment_instance, score, reading_time, answering_time)

        # AssessmentSession model
        assessment_instance.total_score = assessment_instance.assessment_passage.aggregate(total_score=models.Sum('score'))['total_score'] or 0
        assessment_instance.total_reading_time = assessment_instance.assessment_passage.aggregate(total_reading_time=models.Sum('reading_time'))['total_reading_time'] or 0
        assessment_instance.total_answering_time = assessment_instance.assessment_passage.aggregate(total_answering_time=models.Sum('answering_time'))['total_answering_time'] or 0
        assessment_instance.end_time = timezone.now()
        assessment_instance.is_finished = True
        assessment_instance.save()

        calculate_overall_rating(student_instance, assessment_instance)

        messages.success(request, 'Assessment done.')
        return redirect('assessment_done', assessment_id = assessment_instance.id)

    context = {
        'type': 'Graded',
        'assessment_instance': assessment_instance,
        'passage_instance': passage_instance,
        'question_forms': question_forms,
    }

    return render(request, 'assessment/student/assessment.html', context)