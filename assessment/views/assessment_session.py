from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from read_app.models import User
from materials.models import Passage, Choice
from assessment.models import AssessmentSession, AssessmentSessionPassage, StudentAnswer

from assessment.forms.question import AssessmentQuestionForm

def student_assessment_list(request):
    student_user_instance = get_object_or_404(User, pk=request.user.id)
    student_instance = student_user_instance.student_instance
    assessment_sessions = AssessmentSession.objects.filter(student=student_instance, is_finished=False)
    context = {
        'assessment_sessions': assessment_sessions,
    }
    return render(request, 'assessment/student/assessment_list.html', context)


def screening_assessment_start(request, assessment_id):
    assessment_instance = get_object_or_404(AssessmentSession, pk=assessment_id)
    assessment_passage_instances = assessment_instance.get_passages()
    passage_question_sets = [] 
    

    for assessment_passage_instance in assessment_passage_instances:
        number_of_questions = assessment_passage_instance.passage.number_of_questions
        question_set = assessment_passage_instance.passage.get_questions()
        passage_question_sets.append((assessment_passage_instance.id, question_set))

    context = {
    }
    return render(request, 'assessment/student/assessment.html', context)


def assessment_view(request, assessment_id):
    assessment_instance = get_object_or_404(AssessmentSession, pk=assessment_id)
    assessment_passage_instances = assessment_instance.get_passages()
    student_user_instance = get_object_or_404(User, pk=request.user.id)
    student_instance = student_user_instance.student_instance
    start_time = timezone.now()

    if assessment_instance.is_finished == True:
        messages.error(request, 'Assessment already finished.')
        return redirect('assessment_list')


    if len(assessment_passage_instances) == 1:
        for assessment_passage_instance in assessment_passage_instances:
            passage_instance = assessment_passage_instance.passage

    questions = passage_instance.get_questions()
    form_instances = [AssessmentQuestionForm(question=question) for question in questions]

    if request.method == 'POST':
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
          
        assessment_instance.is_finished = True
        assessment_instance.start_time = start_time
        assessment_instance.end_time = timezone.now()
        assessment_instance.total_score = score
        assessment_instance.save()

        messages.success(request, 'Answers Submitted.')
        return redirect('assessment_done', assessment_id = assessment_instance.id)

    context = {
        'assessment_id': assessment_id,
        'passage_instance': passage_instance,
        'form_instances': form_instances,
        'questions': questions,
        'start_time': start_time,
    }

    return render(request, 'assessment/student/assessment.html', context)


def assessment_result_view(request, assessment_id):
    assessment_instance = get_object_or_404(AssessmentSession, pk=assessment_id)
    
    student_answers = assessment_instance.get_responses()
    correct_answers = []
    for answer in student_answers:
        question = answer.question
        correct_answers.append({str(question.id): question.get_correct()})

    score = assessment_instance.total_score

    context = {
        'score': score,
        'student_answers': student_answers,
        'assessment_instance': assessment_instance,
    }

    return render(request, 'assessment/student/assessment_result.html', context)


def check_answer(question, answer):
    correct_answer = question.get_correct()
    student_answer = answer
    print('correct:', correct_answer)
    print('student:', student_answer)
    if student_answer == correct_answer:
        return True
    else:
        return False