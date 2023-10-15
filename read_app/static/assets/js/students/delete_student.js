$(document).ready(function() {
    let deleteStudentModal = $('#delete-student-modal');
    
    $('.delete-student-button').click(function() {
        console.log("HELLO!");
        let studentId = $(this).data('student-id');
        let url = `delete_student/${studentId}`;

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response) {
                console.log('HELLO!');
                deleteStudentModal.find('#delete-form-container').html(response);
            },
            error: function(error) {
                console.error(error);
            }
        });
    });
});