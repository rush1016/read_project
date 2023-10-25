$(document).ready(function() {
    const editButton = $('.edit-student-btn');
    const deleteButton = $('.delete-student-btn');

    function buttonClickChecker() {
        // Check for button clicks and call the function
        editButton.click(function() {
            fillFormFields($(this));
        });

        deleteButton.click(function() {
            fillFormFields($(this));
        }); 
    }

    function fillFormFields(button) {
        let studentId = button.data('student-id');
        let modalForm = $('#deleteStudentForm');
        let submitFormUrl = "delete_student";

        // If edit button is clicked, then fill the edit form instead
        if (button.hasClass('edit-student-btn')) {
            modalForm = $('#editStudentForm');
            submitFormUrl = "edit_student";
        }
        
        getSingleStudentRecord(studentId)
        // If successful in fetching data
        .then(function(studentRecord) {
    
            // Change the url to use student id        
            modalForm.attr('action', `${submitFormUrl}/0`.replace('0', studentId));
            
            // Fill the form fields with the fetched data
            modalForm.find('#id_first_name').val(studentRecord['first_name']);
            modalForm.find('#id_last_name').val(studentRecord['last_name']);
            modalForm.find('#id_grade_level').val(studentRecord['grade_level']);
            modalForm.find('#id_class_section').val(studentRecord['class_section']);
        })

        // If fail in fetching data
        .catch(function(error) {
            console.error('Error:', error);
        })
    }


    // Function call
    buttonClickChecker();
});