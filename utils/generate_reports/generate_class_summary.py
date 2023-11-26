import io
import pandas as pd
from django.http import HttpResponse

from read_app.models import User
from students.models import Student

def generate_class_summary(teacher_id, language):
    teacher_user = User.objects.get(pk=teacher_id)
    teacher = teacher_user.teacher
    students = Student.objects.filter(teacher=teacher_user).order_by('last_name')
    if language == 'English':
        gst_scores = [student.student_rating.english_gst_score for student in students]
        ratings = [student.student_rating.english_rating for student in students]
    elif language == 'Filipino':
        gst_scores = [student.student_rating.filipino_gst_score for student in students]
        ratings = [student.student_rating.filipino_rating for student in students]

    # Create a DataFrame from the queryset
    data = {
        'Last Name': [student.full_name() for student in students],
        'Screening Test Score': gst_scores,
        'Graded Assessments Done': [student.assessments_done for student in students],
        'Reading Level': ratings,
    }

    df = pd.DataFrame(data)

    buffer = io.BytesIO()

    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        sheet_name = f'GRADE_{teacher.grade_level}_{teacher.section}_CLASS_SUMMARY'
        # Convert the dataframe to an XlsxWriter Excel object
        df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=2)

        # Get the xlsxwriter workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]

        # Write the header with merged cells
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'vcenter',
            'align': 'center',
            'border': 1,
            'fg_color': '#D7E4BC',  # Set background color
        })

        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)

        # Merge the cells for the first row
        worksheet.merge_range('A1:D1', f'Screening Test Class Reading Record ({language})', header_format)

        # Iterate through all columns and set the width to the maximum length of data in each column
        for i, col in enumerate(df.columns):
            max_len = df[col].astype(str).map(len).max()
            max_len = max_len if max_len > len(col) else len(col)  # account for header length
            worksheet.set_column(i, i, max_len + 2)  # add a little extra space

    # Set the buffer's position to the start
    buffer.seek(0)

    # Create a response with the file
    response = HttpResponse(buffer.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=class_summary.xlsx'

    return response