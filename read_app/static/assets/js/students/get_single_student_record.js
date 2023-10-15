function getSingleStudentRecord(studentId) {
    return $.ajax({
        url: '/get_student_info/' + studentId,
        type: 'GET',
    })
    .then(function(response) {
        return response.student_data;
    })
    .fail(function(error) {
        console.error('Error fetching student data:', error);
    });
}