function getClassSectionData() {
    let classSectionData = null;

    $.ajax({
        url: 'get_class_section_data/',
        type: 'GET',
        async: false,
        success: function(response) {
            classSectionData = response.class_section_data;
        },
        error: function(error) {
            console.error('Error fetching class section data:', error);
        }
    });
    return classSectionData;
}