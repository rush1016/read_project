$(document).ready(function() {
    let approveFormContainer = $('#approve-form-container');
    $('.approve-student-button').click(function() {
        let studentId = $(this).data('student-id');
        let url = `approve/${studentId}`;

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                approveFormContainer.html(response);
            },
            error: function(error) {
                console.error(error);
            }
        })
    });
});