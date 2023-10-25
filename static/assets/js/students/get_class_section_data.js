function getClassSectionData() {
    return $.ajax({
        url: 'get_class_section_data/',
        type: 'GET',
    })
    .then(function(response) {
        return response.class_section_data;
    })
    .fail(function(error) {
        console.error('Error fetching class section data:', error);
    });
}