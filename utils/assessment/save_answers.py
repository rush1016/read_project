from django.shortcuts import get_object_or_404

from materials.models import Choice
from assessment.models import StudentAnswer
from utils.assessment.check_answer import check_answer

def save_answers(request, assessment_instance, passage_instance, student_instance, questions):
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
        student_answer_instance = StudentAnswer.objects.get_or_create(
            assessment=assessment_instance,
            student=student_instance,
            passage=passage_instance,
            question=question,
        )
        student_answer_instance[0].answer = choice_instance
        student_answer_instance[0].correct = correct=correct
        student_answer_instance[0].save()

    return score
            