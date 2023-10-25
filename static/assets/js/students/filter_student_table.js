$(document).ready(function() {
    const gradeFilterField = '#filter-container #id_grade_level';
    const sectionFilterField = '#filter-container #id_class_section';
    const filterResetButton = $('#filter-container #filter-reset-button');
    
    $(`${gradeFilterField}, ${sectionFilterField}`).change(function() {
        filterStudentRecords();
        updateSectionOptions(gradeFilterField, sectionFilterField);
    });

    function filterStudentRecords() {
        let selectedGradeLevel = $(gradeFilterField).val();
        let selectedSection = $(sectionFilterField).val();
        
        $('#studentList tbody tr').each(function() {
            let row = $(this);
            let gradeInRow = row.find('td:eq(4)').text().trim().replace('Grade ', '');
            let sectionInRow = row.find('td:eq(5)').text().trim();

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


    filterResetButton.click(function() {
        $(gradeFilterField).val($(gradeFilterField).find('option:first').val());
        $(sectionFilterField).val($(sectionFilterField).find('option:first').val());
        filterStudentRecords();
    });
})