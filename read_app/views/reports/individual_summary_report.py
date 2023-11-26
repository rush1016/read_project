from django.shortcuts import redirect
from django.contrib import messages

from utils.generate_reports.generate_individual_summary import generate_isr_word_document

def generate_report(request, student_id):
    language = request.POST.get('selected-language')
    generated_report = generate_isr_word_document(student_id, language)

    if generated_report:
        messages.success(request, 'Successfully generated report.')
        return generated_report
    
    else:
        messages.error(request, 'Report cannot be generated. Student may not have finished assessments for the selected language.')
        return redirect('student_profile', student_id)