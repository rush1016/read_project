from assessment.models import StudentAnswer

class IsrSetup():
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




    def set_level_started(assessments, table):
        first_assessment_grade_level = assessments[0].grade_level
        i = 1
        for row in table.rows[2:]:
            if i == first_assessment_grade_level:
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