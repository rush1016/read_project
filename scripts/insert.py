import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "..read_project.settings")
django.setup()

from read_app.models import Grade, ClassSection

def insert_grade():
    for i in range(4, 6):
        Grade.objects.create(
            grade_level = i,
            grade_name = f'Grade {i}'
        )

CLASS_SECTIONS = {
    4: [
        'Rizal',
        'Bonifacio',
        'Aguinaldo',
        'Luna',
        'Mabini',
    ],
    5: [
        'Marcos',
        'Duterte',
        'Macapagal',
        'Roxas',
        'Garcia',
    ],
    6: [
        'Pluto',
        'Earth',
        'Venus',
        'Jupiter',
    ]
}

def insert_section():
    for grade, sections in CLASS_SECTIONS.items():
        for section in sections:
            ClassSection.objects.create(
                grade_level = grade,
                section_name = section 
            )
    

insert_grade()
insert_section()