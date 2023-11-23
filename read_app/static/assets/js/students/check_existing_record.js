$(document).ready(function () {
    // Intercept the form submission
    $('#modal-add-button').click(function (event) {
        // Get the values from the form
        let firstName = $('#id_first_name').val();
        let middleName = $('#id_middle_name').val();
        let lastName = $('#id_last_name').val();
        let suffix = $('#id_suffix').val();
        let school_id = $('#school-id').val();

        // Check if a student with the same details already exists
        checkExistingStudent(firstName, middleName, lastName, suffix, school_id, function(existingStudent) {
            if (existingStudent) {
                // Display a modal to confirm if the user wants to add the record
                $('#confirm-add-modal').modal('show');
            }
            else {
                $('#add-student-form').submit();
                event.preventDefault();
            }
        });
    });

    // Function to check if a student with the same details already exists
    function checkExistingStudent(firstName, middleName, lastName, suffix, school_id, callback) {
        // Perform an AJAX request to check for an existing student
        $.ajax({
            type: 'GET',
            url: 'check_existing_student', // Replace with the actual URL for your check
            data: {
                'first_name': firstName,
                'middle_name': middleName,
                'last_name': lastName,
                'suffix': suffix,
                'school_id': school_id,
            },
            success: function (data) {
                callback(data.exists);
            }
        });
    }

    // Handling the confirmation modal
    $('#confirm-add-modal-button').click(function() {
        // Submit the form after user confirmation
        $('#add-student-form').submit();
    });
});