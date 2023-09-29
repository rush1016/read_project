$(document).ready(function() {
    $('#filter-grade, #filter-section').change(function() {
        filterStudentRecords();
    });

    function filterStudentRecords() {
        let selectedGradeLevel = $('#filter-grade').val();
        let selectedSection = $('#filter-section').val();
        console.log(selectedGradeLevel);
        $('#studentList tbody tr').each(function() {
            let row = $(this);
            let gradeInRow = row.find('td:eq(2)').text().trim().replace('Grade ', '');
            let sectionInRow = row.find('td:eq(3)').text().trim();

            let gradeMatch = (selectedGradeLevel === '' || gradeInRow === selectedGradeLevel);
            let sectionMatch = (selectedSection === '' || sectionInRow === selectedSection);

            if (gradeMatch && sectionMatch){
                row.show();
            }
            else {
                row.hide();
            }
        })
    }
})