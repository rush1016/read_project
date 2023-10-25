$(document).ready(function() {
    let deleteStudentModal = $('#delete-student-modal');
    
    $('.delete-student-button').click(function() {
        let studentId = $(this).data('student-id');
        let url = `delete/${studentId}`;

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response) {
                deleteStudentModal.find('#delete-form-container').html(response);
            },
            error: function(error) {
                console.error(error);
            }
        });
    });
});