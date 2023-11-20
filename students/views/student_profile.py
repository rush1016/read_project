from django.shortcuts import render, get_object_or_404

from students.models import Student
from materials.models import AssessmentPreset
from assessment.forms.gst_score import GstScoreForm
from students.forms.students import StudentRegistrationForm

def student_profile_view(request, student_id):
    student_instance = get_object_or_404(Student, pk=student_id)
    graded_assessments = student_instance.get_graded()
    screening_assessments = student_instance.get_screening()
    presets = AssessmentPreset.objects.filter(grade_level=student_instance.grade_level)
    gst_score_form = GstScoreForm()
    student_edit_form = StudentRegistrationForm(instance=student_instance)

    context = {
        'student': student_instance,
        'graded_assessments': graded_assessments,
        'screening_assessments': screening_assessments,
        'presets': presets,
        'gst_score_form': gst_score_form,
        'student_edit_form': student_edit_form,
    }

    return render(request, 'students/student_profile.html', context)