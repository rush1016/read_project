$(document).ready(function() {
    let studentLrnField = $('#id_student_lrn');
    let studentLrnToInt = parseInt(studentLrnField.val());

    studentLrnField.val(studentLrnToInt);
});