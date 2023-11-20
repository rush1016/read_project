from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.http import require_GET
from django.http import JsonResponse

from students.forms.students import StudentRegistrationForm
from students.models import Student, StudentRating


def add_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)

        if form.is_valid():
            student = form.save(commit=False)
            student.teacher = request.user
            student.save()

            StudentRating.objects.create(
                student = student,
            )

            messages.success(request, 'Successfully added student record.')
            return redirect('student_list')
        else:
            messages.error(request, form.errors)
            return redirect('student_list')
        
    
@require_GET
def check_existing_student(request):
    first_name = request.GET.get('first_name')
    middle_name = request.GET.get('middle_name')
    last_name = request.GET.get('last_name')
    suffix = request.GET.get('suffix')

    # Perform a query to check if a student with the given details exists
    existing_student = Student.objects.filter(
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        suffix=suffix
    ).exists()

    print(existing_student)

    return JsonResponse({'success': True, 'exists': existing_student})