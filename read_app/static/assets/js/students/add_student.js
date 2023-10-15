$(document).ready(function() {
  const addStudentForm = $('#addStudentForm');
  const confirmationModal = new bootstrap.Modal(document.getElementById('confirmationModal'));

  addStudentForm.on('submit', function(event) {
    event.preventDefault();

    $.ajax({
      type: 'POST',
      url: 'add_student',
      data: addStudentForm.serialize(),
      dataType: 'json',
      success: function(response) {
        
        // A matching archived student record exists, show the confirmation modal
        if (response.archived_student_id) {
          confirmationModal.show();
          console.log(response.archived_student_id);
          $('#confirmButton').click(function() {
            window.location.href = 'confirm_add_archived_student/' + response.archived_student_id;
            
            // Close the confirmation modal
            confirmationModal.hide();
          });
        } else if (response.success) {
          window.location.href = 'add_student';
          // Student added successfully, close the "Add Student" modal
          $('#addStudentModal').modal('hide');

        } else {
          // Handle form validation errors if needed
          console.log(response.errors);
        }
      },
      error: function(error) {
        console.error('Error:', error);
      }
    });
  });
});