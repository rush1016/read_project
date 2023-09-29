$(document).ready(function() {
    let classSectionData = getClassSectionData();
    
    function updateOptions(idModal) {
        const selectedGradeLevel = $(`${idModal} #id_grade_level`).val();

        // Iterate through each options of class_section field within the current modal
        // 
        $(`${idModal} #id_class_section option`).each(function() {
            const gradeLevelAttribute = $(this).attr('data-grade-level');
            if (gradeLevelAttribute !== selectedGradeLevel) {
                $(this).hide();
            } 
            else {
                $(this).show();
            }
        });
    }


    function createGradeLevelMapping() {
        const gradeLevelMapping = {};

        // Generate the mapping from class_section_data
        classSectionData.forEach(item => {
            gradeLevelMapping[item.section_name] = item.grade_level;
        });

        return gradeLevelMapping;
    }


    // Function to set the data-grade-level attribute
    // To be used as reference which options to hide and show
    function setGradeLevelAttribute(idModal) {
        const gradeLevelMapping = createGradeLevelMapping();
    
        // Iterate through the list and assign the 
        // value into data-grade-level attribute
        $(`${idModal} #id_class_section option`).each(function() {
            let classSectionName = $(this).val();

            if (gradeLevelMapping.hasOwnProperty(classSectionName)) {
                let gradeLevel = gradeLevelMapping[classSectionName];
                $(this).attr('data-grade-level', gradeLevel);
            }
        });
        // Initial update of options
        updateOptions(idModal);
    }


    // Function to initiate the modal form when modal is opened
    function initializeModal(idModal) {
        const gradeLevelField = $(`${idModal} #id_grade_level`);
        const classSectionField = $(`${idModal} #id_class_section`);
        
        // Add an empty selection to add student modal form
        classSectionField.prepend('<option value="" selected>Select Section</option>');
        
        // Call the function to set the data-grade-level attribute
        setGradeLevelAttribute(idModal);
        
        // Listen for changes in the grade_level field
        gradeLevelField.change(function() {
            // Reset the select field within the current modal
            $(`${idModal} #id_class_section`).val('');
            updateOptions(idModal);
        });

        // Update the options when the modal is opened
        $(idModal).on('shown.bs.modal', function () {
            updateOptions('#editStudentModal');
        });
    }
  

    // Initialize the modals
    initializeModal('#addStudentModal');
    initializeModal('#editStudentModal');
});