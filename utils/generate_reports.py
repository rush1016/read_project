from django.http import HttpResponse

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL

from students.models import Student
from assessment.models import AssessmentSession, StudentAnswer


def set_level_column(table, col_index=1):
    levels = [
        'I',
        'II',
        'III',
        'IV',
        'V',
        'VI',
        'VII',
    ]

    # Start from the second column (index 1) and the third row (index 2)
    row_index = 2

    for level in levels:
        cell = table.cell(row_index, col_index)
        cell.text = level
        row_index += 1


def set_cell_center(table):
    for row in table.rows:
        cells = row.cells
        # Set the alignment of text in each cell to center
        for cell in cells:
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

            for paragraph in cell.paragraphs:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER


def set_level_started(assessments, table):
    first_assessment_grade_level = assessments[0].grade_level
    i = 1
    for row in table.rows[2:]:
        if i == first_assessment_grade_level:
            print("True")
            row.cells[0].text = '*'
        i += 1


def set_reading_rating(assessments, table):
    for assessment in assessments:
        row = assessment.grade_level+1
        date_col = 9
        set_col = 2
        date = assessment.end_time.strftime('%d %B')
        set = assessment.get_graded_passage().passage.set

        word_reading = assessment.graded_assessment.oral_reading_rating
        comprehension = assessment.graded_assessment.reading_comprehension_rating

        if word_reading == "Independent":
            word_reading_col = 3
        elif word_reading == "Instructional":
            word_reading_col = 4
        else:
            word_reading_col = 5

        if comprehension == "Independent":
            comprehension_col = 6
        elif comprehension == "Instructional":
            comprehension_col = 7
        else:
            comprehension_col = 8

        table.cell(row, word_reading_col).text = '✔'
        table.cell(row, comprehension_col).text = '✔'
        table.cell(row, date_col).text = date
        table.cell(row, set_col).text = set


def set_passage_data(assessments, table):
    for assessment in assessments:
        row = assessment.grade_level+1
        score_col = 9
        reading_percentage_col = 10
        reading_level_col = 11

        passage = assessment.get_graded_passage().passage
        questions = passage.get_questions()
        i = 1

        for question in questions:
            student_answer = StudentAnswer.objects.filter(assessment=assessment, question=question).first()
            if student_answer.correct:
                table.cell(row, i).text = '✔'
            else:
                table.cell(row, i).text = 'X'
            i += 1

        table.cell(row, score_col).text = f'{assessment.total_score}/{assessment.number_of_questions}'
        table.cell(row, reading_percentage_col).text = f'{round(float(assessment.graded_assessment.reading_comprehension_score))}'
        table.cell(row, reading_level_col).text = f'{assessment.graded_assessment.reading_comprehension_rating}'

class GenerateReports():
    @staticmethod
    def generate_isr_word_document(student_id, language):
        student = Student.objects.get(pk=student_id)
        age = str(student.age)
        assessments = AssessmentSession.objects.filter(
            student=student, 
            assessment_type="Graded", 
            assessment_passage__passage__language=language,
        ).order_by('end_time')

        doc = Document()

        doc.styles['Normal'].font.name = 'Arial'
        doc.styles['Normal'].font.size = Pt(11)

        # Add a centered heading with custom font and font size
        title = doc.add_paragraph('Individual Summary Record (ISR)')
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        title_run = title.runs[0]
        title_run.font.size = Pt(13)
        title_run.bold = True
        
        title2 = doc.add_paragraph('Talaan ng Indibidwal na Pagbabasa (TIP)')
        title2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        title2_run = title2.runs[0]
        title2_run.font.size = Pt(13)
        title2_run.italic = True

        whitespace = doc.add_paragraph(' ')
        whitespace.runs[0].font.size = Pt(8.5)

        # Student Info
        info_line_1 = doc.add_paragraph('Name: ')
        info_line_1.add_run(f'{student.first_name} {student.last_name}').underline = True
        info_line_1.add_run('       Age: ')
        info_line_1.add_run(age).underline = True
        info_line_1.add_run(f'                          Grade/Section: ')
        info_line_1.add_run(f'{student.grade_level}-{student.class_section}').underline = True

        info_line_2 = doc.add_paragraph('School: ')
        info_line_2.add_run('Sapalibutad Elementary School').underline = True
        info_line_2.add_run('                           Teacher: ')
        info_line_2.add_run(f'{student.teacher}').underline = True

        if language == 'Filipino':
            info_line_3 = doc.add_paragraph('English: ☐ ')
            info_line_3.add_run('       Filipino: ☑')
        elif language == 'English':
            info_line_3 = doc.add_paragraph('English: ☑ ')
            info_line_3.add_run('       Filipino: ☐')
        
        for run in info_line_3.runs:
            run.bold = True

        records = (
            (3, '101', 'Spam'),
            (7, '422', 'Eggs'),
            (4, '631', 'Spam, spam, eggs, and spam')
        )


        # Table
        table = doc.add_table(rows=9, cols=10)
        table.style = 'Table Grid'
        hdr_row = table.rows[0]
        hdr2_row = table.rows[1]

        # Table Header First Layer 
        hdr_row.cells[3].merge(hdr_row.cells[5])
        hdr_row.cells[6].merge(hdr_row.cells[8])

        hdr_row.cells[0].text = 'Level Started'
        hdr_row.cells[1].text = 'Level'
        hdr_row.cells[2].text = 'Set'
        hdr_row.cells[3].text = 'Word Reading'
        hdr_row.cells[6].text = 'Comprehension'
        hdr_row.cells[9].text = 'Date Taken'

        for cell in hdr_row.cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.bold = True
        # End First Layer

        # Table Header Second Layer
        hdr2_row.cells[0].text = 'Mark with an *'
        hdr2_row.cells[1].text = ''
        hdr2_row.cells[2].text = 'Indicate if A. B. C. or D.'
        hdr2_row.cells[3].text = 'Ind'
        hdr2_row.cells[4].text = 'Ins'
        hdr2_row.cells[5].text = 'Frus'
        hdr2_row.cells[6].text = 'Ind'
        hdr2_row.cells[7].text = 'Ins'
        hdr2_row.cells[8].text = 'Frus'
        hdr2_row.cells[9].text = ''
        # End Second Layer

        # Set the values for LEVEL column
        set_level_column(table)

        set_reading_rating(assessments, table)

        set_level_started(assessments, table)

        set_cell_center(table)

        legend = doc.add_paragraph('Legend: Ind- ')
        legend.runs[0].bold = True
        legend.add_run('Independent; ')
        legend.add_run('Ins- ').bold = True
        legend.add_run('Instructional; ')
        legend.add_run('Frus- ').bold = True
        legend.add_run('Frustration')

        # Add Line Break 
        doc.add_paragraph()

        page2_subtitle = doc.add_paragraph('Summary of Comprehension Responses')
        page2_subtitle.add_run('(Talaan ng Pag-unawa)')
        page2_subtitle.runs[0].bold = True


        # Table 
        page2_table = doc.add_table(rows=9, cols=12)
        page2_table.style = 'Table Grid'

        header = page2_table.rows[0]

        header.cells[0].text = 'Passage Level'
        header.cells[1].merge(header.cells[8])
        header.cells[1].text = 'Responses to Questions'
        header.cells[9].text = 'Score'
        header.cells[10].text = '%'
        header.cells[11].text = 'Reading Level'

        row3 = page2_table.rows[1]
        row3.cells[0].text = ' '

        for i in range(1, 9):
            row3.cells[i].text = f'Q{i}'

        set_level_column(page2_table, col_index=0) 

        set_passage_data(assessments, page2_table)

        set_cell_center(page2_table)


        # Save the document in-memory
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename=Individual_Summary_Record_for_{student.last_name}_{student.first_name}.docx'
        doc.save(response)

        return response