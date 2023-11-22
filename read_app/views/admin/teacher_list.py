from django.shortcuts import render

from read_app.models import School, Teacher

def teacher_list_view(request):
    school = School.objects.get(school_code=107037)
    teacher_list = Teacher.objects.filter(school=school)

    context = {
        'teachers': teacher_list,

    }

    return render(request, 'teachers/teacher_list.html', context)