from django.shortcuts import render

from read_app.models import School, Teacher

def teacher_list_view(request, school_id):
    school = School.objects.get(pk=school_id)
    teacher_list = Teacher.objects.filter(school=school).order_by('grade_level', 'section')

    context = {
        'teachers': teacher_list,

    }

    return render(request, 'admin/teacher_list.html', context)