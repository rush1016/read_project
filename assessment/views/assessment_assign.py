from django.shortcuts import redirect, get_object_or_404, get_list_or_404
from django.contrib import messages
from django.db import transaction

from read_app.models import User
from students.models import Student
from assessment.models import ( 
    AssessmentSession, 
    AssessmentSessionPassage, 
    ScreeningAssessment, 
    GradedAssessment 
)
from materials.models import Passage, AssessmentPreset
from utils.generate_passcode import generate_passcode

@transaction.atomic
def assign_assessment(request, assessment_type):
    if request.method == 'POST':
        student_list = request.POST.getlist('selected_records')

        for student in student_list:
            student_instance = get_object_or_404(Student, pk=student)
            passcode = generate_passcode() # 6-digit passcode

            # Create the assessment session record to be saved into the database
            assessment_session = AssessmentSession.objects.create(
                student = student_instance,
                assessment_type = assessment_type,
                grade_level = student_instance.grade_level, 
                passcode = passcode,
            )

            grade_level = assign_assessment_type(assessment_session, request)
            assessment_session.grade_level = grade_level
            assessment_session.save()

            if assessment_session.assessment_type == "Graded":
                return redirect('assessment_session', assessment_session.id)

            messages.success(request, f'Successfully assigned assessment.\nCopy this code to and enter it in the assessment code field: {assessment_session.passcode}')

    return redirect('assessment_select')

# Assign assessment based on type
def assign_assessment_type(assessment_session, request):
    if assessment_session.assessment_type == 'Screening':
        preset_id = request.POST.get('preset_select')
        grade_level = assign_screening(assessment_session, preset_id)
        assessment_session.student.screening = True
        assessment_session.student.save()

    elif assessment_session.assessment_type == 'Graded':
        passage_id = request.POST.get('passage_id')
        grade_level = assign_graded(assessment_session, passage_id)
        
    return grade_level
        

def assign_screening(assessment_session, preset_id):
    preset = get_object_or_404(AssessmentPreset, pk=preset_id)
    passages = get_list_or_404(Passage, preset=preset)
    total_questions = 0
    order = 1
    # Simple algorithm for adding order of passages to be taken
    # This will be used later for rendering the passages in screening assessment
    for passage in passages:
        create_assessment_session_passage(assessment_session, passage, order)
        order += 1
        total_questions += len(passage.get_questions())


    assessment_session.number_of_questions = total_questions
    assessment_session.save()

    screening_assessment_instance = ScreeningAssessment.objects.create(
        assessment_session = assessment_session
    )
    # This counts the different types of questions and set them into the ScreeningAssessment record/instance
    # Question types are: Literal, Inferential, and Critical
    screening_assessment_instance.update_question_counts() 

    return preset.grade_level


def assign_graded(assessment_session, passage_id):
    # Graded Passage Assessment is only taking 1 passage per assessment
    passage_instance = get_object_or_404(Passage, pk=passage_id)
    assessment_session.number_of_questions = len(passage_instance.get_questions())
    assessment_session.save()

    create_assessment_session_passage(assessment_session, passage_instance, 1)

    GradedAssessment.objects.create(
        assessment_session = assessment_session
    )
    return passage_instance.grade_level    


def create_assessment_session_passage(assessment_session, passage, order):
    # This function creates an AssessmentSessionPassage record
    # This is a separate table that has relation to both AssessmentSession table
    # And Passage table, to save which passages are being used for the assessment
    # And to get the information from the main table of Passage
    AssessmentSessionPassage.objects.create(
        assessment_session = assessment_session,
        order = order,
        passage = passage,
    )