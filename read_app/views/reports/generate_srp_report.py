from django.shortcuts import redirect
from django.contrib import messages

from utils.generate_reports import GenerateReports

def generate_srp_report_view(request):
    generated_report = GenerateReports.generate_school_reading_profile()

    return generated_report 