from utils.generate_reports import GenerateReports

def download_report(request, student_id):
    language = request.POST.get('selected-language')
    print(language)
    return GenerateReports.generate_isr_word_document(student_id, language)