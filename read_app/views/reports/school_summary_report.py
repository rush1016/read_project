from django.shortcuts import redirect
from django.contrib import messages

from utils.generate_reports.generate_school_summary import generate_school_reading_profile

def generate_report(request, school_id):
    generated_report = generate_school_reading_profile(school_id)

    return generated_report 