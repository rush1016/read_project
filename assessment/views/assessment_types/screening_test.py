from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db import transaction, models

from materials.models import Choice
from students.models import Student
from assessment.models import AssessmentSession, ScreeningAssessment, StudentAnswer
from assessment.views.check_answer import check_answer
from utils.update_passage_data import update_assessment_passage_data
from utils.screening_test_calculations import ScreeningTestCalculations

from assessment.forms.question import AssessmentQuestionForm


@transaction.atomic
def screening_assessment_view(request, assessment_id, order):
    # Assessment
    assessment_instance = get_object_or_404(AssessmentSession, pk=assessment_id)
    screening_instance = assessment_instance.screening_assessment
    assessment_passages = assessment_instance.get_passages()

    # Passage
    current_passage = assessment_passages.get(order=order)
    passage_instance = current_passage.passage

    # Questions
    questions = passage_instance.get_questions()
    question_forms = {}

    for question in questions:
        # Find the student's answer on the current question for the passage
        existing_answer = StudentAnswer.objects.filter(
            assessment = assessment_instance,
            question = question
        ).first()

        form = AssessmentQuestionForm(
            question=question,
            selected_choice_id = existing_answer.answer.id if existing_answer else None
        )

        question_forms[question] = form 


    # Set the current_passage field into the latest submitted passage
    if order == None:
        order = screening_instance.current_passage
    else:
        screening_instance.current_passage = order
        screening_instance.save()


    # Set the start_time to when the user first clicked the begin button
    if assessment_instance.start_time == None:
        assessment_instance.start_time = timezone.now()
        assessment_instance.save()
    

    # Check if assessment is already finished
    if assessment_instance.is_finished == True:
        messages.error(request, 'Assessment already finished.')
        return redirect('assessment_code')
    
    
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
        student_instance = assessment_instance.student
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

            # Save or update student answer
            student_answer_instance = StudentAnswer.objects.get_or_create(
                assessment=assessment_instance,
                student=student_instance,
                passage=passage_instance,
                question=question,
            )
            student_answer_instance[0].answer=choice_instance 
            student_answer_instance[0].correct = correct
            student_answer_instance[0].save()

        # AssessmentSessionPassage model
        # Update recorded assessment values for each passage
        update_assessment_passage_data(passage_id, assessment_instance, score, reading_time, answering_time)

        order += 1

        if order > len(assessment_passages):
            # Screening Assessment model
            screening_instance = get_object_or_404(ScreeningAssessment, assessment_session = assessment_instance)

            screening_instance.correct_literal = get_question_type_count(assessment_instance, 'Literal')
            screening_instance.correct_inferential = get_question_type_count(assessment_instance, 'Inferential')
            screening_instance.correct_critical = get_question_type_count(assessment_instance, 'Critical')

            screening_instance.save()


            # AssessmentSession model
            assessment_instance.total_score = assessment_instance.assessment_passage.aggregate(total_score=models.Sum('score'))['total_score'] or 0
            assessment_instance.total_reading_time = assessment_instance.assessment_passage.aggregate(total_reading_time=models.Sum('reading_time'))['total_reading_time'] or 0
            assessment_instance.total_answering_time = assessment_instance.assessment_passage.aggregate(total_answering_time=models.Sum('answering_time'))['total_answering_time'] or 0
            assessment_instance.is_finished = True
            assessment_instance.end_time = timezone.now()

            student_instance.gst_score = assessment_instance.total_score
            student_instance.screening = False
            student_instance.save()
            assessment_instance.save()

            # Calculate if student needs further assessment or passed the GST
            ScreeningTestCalculations.calculate_screening_rating(assessment_instance)

            ScreeningTestCalculations.calculate_screening_scores(student_instance, assessment_instance)

            messages.success(request, 'Assessment done.')
            return redirect('assessment_done', assessment_id=assessment_instance.id)

        return redirect('screening_assessment', assessment_id=assessment_id, order=order)
    

def get_question_type_count(assessment_instance, question_type):
    count = StudentAnswer.objects.filter(
        assessment = assessment_instance,
        correct = True,
        question__question_type = question_type,
    ).count()

    return count

