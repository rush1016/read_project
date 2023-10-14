from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404

from read_app.models import Passage

def get_passage_info(request, passage_id):

    try:
        # Retrieve the student record
        passage_instance = get_object_or_404(Passage, id=passage_id)
        
        passage_data = {
            'passage_id': passage_instance.id,
            'passage_title':passage_instance.passage_title,
            'passage_content': passage_instance.passage_content,
            'grade_level': passage_instance.grade_level,
        }

        return JsonResponse({'success': True, 'passage_data': passage_data})

    except Http404:
        # Handle the case where the student record is not found
        return JsonResponse({'success': False, 'error': 'Student not found'}, status=404)