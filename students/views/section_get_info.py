from django.http import JsonResponse
from students.models import ClassSection


def get_class_section_data(request):
    try:
        class_section_data = list(ClassSection.objects.values('grade_level', 'section_name'))
        return JsonResponse({'class_section_data': class_section_data})

    except Exception as e:
        # Handle any exceptions that might occur during database query or JSON serialization
        return JsonResponse({'success': False, 'error': str(e)}, status=500)