def check_answer(question, answer):
    correct_answer = question.get_correct()
    student_answer = answer

    if student_answer == correct_answer:
        return True
    else:
        return False
    