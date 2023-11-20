from django.shortcuts import redirect
from django.contrib import messages

from assessment.forms.gst_score import GstScoreForm
from students.models import Student
from utils.screening_test_calculations import ScreeningTestCalculations

def add_gst_score(request, student_id):
    form = GstScoreForm()    

    if request.method == 'POST':
        student = Student.objects.get(pk=student_id)
        form = GstScoreForm(request.POST)
        if form.is_valid():

            gst_score = int(form.cleaned_data['gst_score'])
            language = form.cleaned_data['language']

            ScreeningTestCalculations.calculate_screening_rating_add(student, gst_score, language)
            
            messages.success(request, 'Successfully added GST score')
        else:
            messages.error(request, form.errors['gst_score'])

    return redirect('student_profile', student.id)