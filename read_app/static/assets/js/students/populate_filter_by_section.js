$(document).ready(function() {
    async function populateFilterBySection() {
        try {
            const classSectionData = await getClassSectionData();
            const classSectionFilter = $('#id_class_section');

            classSectionFilter.append("<option value=''>All</option>");

            classSectionData.forEach(sectionData => {
                classSectionFilter.append(`<option value="${sectionData.section_name}" data-grade-level="${sectionData.grade_level}">${sectionData.section_name}</option>`);
            });
        }
        catch(error) {
            console.error('Error: ', error)
        }
    };

    populateFilterBySection();
});