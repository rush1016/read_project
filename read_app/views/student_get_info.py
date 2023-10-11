from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from read_app.models import Student, User


# For fetching data from the database
def get_student_info(request, student_id):
    try:
        # Retrieve the student record
        student_user_instance = get_object_or_404(User, pk=student_id)
        student = get_object_or_404(Student, pk=student_user_instance)
        student_data = {
            'id': student.student_id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'grade_level': student.grade_level,
            'class_section': student.class_section, 
        }

        return JsonResponse({'success': True, 'student_data': student_data})

    except Http404:
        # Handle the case where the student record is not found
        return JsonResponse({'success': False, 'error': 'Student not found'}, status=404)