$(document).ready(function() {
    let editStudentModal = $('#edit-student-modal');

    // Open the modal for edit student form
    $('.edit-student-btn').click(function(){
        let studentId = $(this).data('student-id');
        let url = `edit_student/${studentId}`;
        
        $.get(url, function(response){
            editStudentModal.find('#edit-form-container').html(response);
        });
    });

});