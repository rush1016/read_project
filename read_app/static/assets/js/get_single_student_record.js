function getSingleStudentRecord(studentId) {
    let studentRecord = null; 
    
    // AJAX request to retrieve student data based on the studentId
    $.ajax({
        url: '/get_student_info/' + studentId,
        type: 'GET',
        async: false,
        success: function(response) {
            studentRecord = response.data;
        },
        error: function(error) {
            console.error('Error fetching class section data:', error);
        }
    }); // End Ajax

    return studentRecord;
}