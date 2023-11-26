$(document).ready(function() {
    let gradeFilterField = $('#reading-filter-container #grade-level');
    let filterResetButton = $('#filter-reset-button');

    gradeFilterField.change(function() {
        filterReadingMaterial();
    });

    filterResetButton.click(function() {
        gradeFilterField.val('');
        filterReadingMaterial();
    });

    function filterReadingMaterial() {
        let selectedGradeLevel = $(gradeFilterField).val();
        
        $('#reading-list tbody tr').each(function() {
            let row = $(this);
            let gradeInRow = row.find('td:eq(4)').text().trim().replace('Grade ', '');
            console.log(gradeInRow)
            let gradeMatch = (selectedGradeLevel === '' || gradeInRow === selectedGradeLevel);
            
            if (gradeMatch){
                row.show();
            }
            else {
                row.hide();
            }
        })
    }
});