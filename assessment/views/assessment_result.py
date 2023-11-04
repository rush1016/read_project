from django.shortcuts import render, get_object_or_404

from assessment.models import AssessmentSession

def assessment_result_view(request, assessment_id):
    assessment_instance = get_object_or_404(AssessmentSession, pk=assessment_id)
    assessment_passages = assessment_instance.get_passages()
    
    score = assessment_instance.total_score

    student_answers_dict = {}

    for passage in assessment_passages:
        passage_instance = passage.passage # Reverse relation
        student_answers = list(assessment_instance.student_answer.filter(passage=passage_instance))
        student_answers_dict[passage_instance] = student_answers

    print(student_answers_dict)
    context = {
        'score': score,
        'student_answers': student_answers_dict,
        'assessment_instance': assessment_instance,
    }

    return render(request, 'assessment/student/assessment_result.html', context)

