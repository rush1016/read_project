from django.shortcuts import redirect
from django.contrib import messages

from read_app.models import User
from students.models import Student
from utils.generate_reports.generate_class_summary import generate_class_summary

def generate_report(request, teacher_id):
    teacher_user = User.objects.get(pk=teacher_id)
    students = Student.objects.filter(teacher=teacher_user).exists()
    language = request.POST.get('selected-language')
    
    if not students:
        messages.error(request, 'There are currently ZERO student records. Class Summary cannot be generated.')
        return redirect('student_list')
    
    generated_report = generate_class_summary(teacher_id, language)

    if generated_report:
        return generated_report
    
    else:
        messages.error(request, 'Report cannot be generated. Student may not have finished assessments for the selected language.')
        return redirect('student_list')