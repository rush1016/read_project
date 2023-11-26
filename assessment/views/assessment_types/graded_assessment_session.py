from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db import transaction


from materials.models import Passage
from assessment.models import AssessmentSession
from utils.assessment.update_passage_data import update_assessment_passage_data
from utils.assessment.update_assessment_data import update_assessment_data
from utils.assessment.save_answers import save_answers

from assessment.forms.question import AssessmentQuestionForm


@transaction.atomic
def graded_assessment_view(request, assessment_id):
    assessment_instance = get_object_or_404(AssessmentSession, pk=assessment_id)
    assessment_passage = assessment_instance.get_graded_passage() # From AssessmentPassages
    passage_instance = assessment_passage.passage # From the main table/model with the content
    questions = passage_instance.get_questions()
    question_forms = {question: AssessmentQuestionForm(question=question) for question in questions}

    student_instance = assessment_instance.student
    
    # Set the start_time to when the user first clicked the begin button
    if assessment_instance.start_time == None:
        assessment_instance.start_time = start_time = timezone.now()
        assessment_instance.save()
    else:
        start_time = assessment_instance.start_time

    # Check if assessment is already finished
    if assessment_instance.is_finished == True:
        messages.error(request, 'Assessment already finished.')
        return redirect('assessment_code')

    

    # Submission
    if request.method == 'POST':
        passage_id = request.POST.get('passage_id')
        passage_instance = Passage.objects.get(pk=passage_id)
        reading_time = request.POST.get('reading_time')
        answering_time = request.POST.get('answering_time')
        extra_reading_time = request.POST.get('extra_reading_time')
        review_count = request.POST.get('review_count')

        # Process the answers and save them
        score = save_answers(request, assessment_instance, passage_instance, student_instance, questions)

        # AssessmentSessionPassage model
        update_assessment_passage_data(passage_instance, assessment_instance, score, reading_time, answering_time)

        # AssessmentSession model
        update_assessment_data(assessment_instance, extra_reading_time, review_count)

        messages.success(request, 'Assessment done.')
        return redirect('assessment_done', assessment_id = assessment_instance.id)

    context = {
        'type': 'Graded',
        'assessment_instance': assessment_instance,
        'passage_instance': passage_instance,
        'question_forms': question_forms,
    }

    return render(request, 'assessment/student/assessment.html', context)