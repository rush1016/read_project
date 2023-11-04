from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db import transaction, models

from materials.models import Passage, Choice
from assessment.models import AssessmentSession, AssessmentSessionPassage, StudentAnswer
from assessment.views.check_answer import check_answer
from assessment.views.update_passage_data import update_assessment_passage_data

from assessment.forms.question import AssessmentQuestionForm


@transaction.atomic
def screening_assessment_view(request, assessment_id, order):
    # Assessment
    assessment_instance = get_object_or_404(AssessmentSession, pk=assessment_id)
    screening_instance = assessment_instance.screening_assessment

    # Set the current_passage field into the latest submitted passage
    if order == None:
        order = screening_instance.current_passage
    else:
        screening_instance.current_passage = order
        screening_instance.save()


    # Set the start_time to when the user first clicked the begin button
    if assessment_instance.start_time == None:
        assessment_instance.start_time = start_time = timezone.now()
        assessment_instance.save()
    else:
        start_time = assessment_instance.start_time

    assessment_passages = assessment_instance.get_passages()
    
    # Check if assessment is already finished
    if assessment_instance.is_finished == True:
        messages.error(request, 'Assessment already finished.')
        return redirect('student_assessment_list')
    
    # Passage
    current_passage = assessment_passages.get(order=order)
    passage_instance = current_passage.passage

    # Questions
    questions = passage_instance.get_questions()
    question_forms = [AssessmentQuestionForm(question=question) for question in questions]
    
    context = {
        'type': 'Screening',
        'assessment_instance': assessment_instance,
        'passage_instance': passage_instance,
        'question_forms': question_forms,
        'order': order,
    }
    return render(request, 'assessment/student/assessment.html', context)


@transaction.atomic
def screening_save_answers_view(request, assessment_id, order):
    assessment_instance = get_object_or_404(AssessmentSession, pk=assessment_id)
    assessment_passages = assessment_instance.get_passages()
    # Passage
    current_passage = assessment_passages.get(order=order)
    passage_instance = current_passage.passage

    # Questions
    questions = passage_instance.get_questions()
    # ---------------------------------------------------
    if request.method == 'POST':
        student_instance = request.user.student_instance
        passage_id = request.POST.get('passage_id')
        reading_time = request.POST.get('reading_time')
        answering_time = request.POST.get('answering_time')
        score = 0

        # Iterate through each question to check them
        for question in questions:
            # Get the unique field names using the question id
            answer_field_name = f'answer_content_{question.id}'
            answer_id = request.POST.get(answer_field_name)
            choice_instance = get_object_or_404(Choice, pk=answer_id)
            correct = False

            if check_answer(question, choice_instance):
                score += 1
                correct = True

            # Save the answers
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

        order += 1

        if order > len(assessment_passages):
            # AssessmentSession model
            assessment_instance.total_score = assessment_instance.assessment_passage.aggregate(total_score=models.Sum('score'))['total_score'] or 0
            assessment_instance.total_reading_time = assessment_instance.assessment_passage.aggregate(total_reading_time=models.Sum('reading_time'))['total_reading_time'] or 0
            assessment_instance.total_answering_time = assessment_instance.assessment_passage.aggregate(total_answering_time=models.Sum('answering_time'))['total_answering_time'] or 0
            assessment_instance.is_finished = True
            assessment_instance.end_time = timezone.now()
            assessment_instance.student.screening = False
            assessment_instance.student.is_screened = True
            assessment_instance.student.save()
            assessment_instance.save()
            messages.success(request, 'Assessment done.')
            return redirect('assessment_done', assessment_id=assessment_instance.id)

        return redirect('screening_assessment', assessment_id=assessment_id, order=order)
    