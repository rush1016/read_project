// gradeField and sectionField are string values of field IDs
function updateSectionOptions(gradeField, sectionField) {
    const selectedGradeLevel = $(gradeField).val();

    // Iterate through each options of class_section field within the current modal
    $(`${sectionField} option`).each(function() {
        const gradeLevelAttribute = $(this).attr('data-grade-level');
        $(this).show();
        
        // If the grade section matches the selected grade
        if (gradeLevelAttribute != selectedGradeLevel && selectedGradeLevel != '') {
            $(this).hide();
        } 
    });
}

$(document).ready(function() {
    async function fetchClassSectionData() {
        try {
            const classSectionData = await getClassSectionData();
            return classSectionData;
        }
        catch(error) {
            console.error('Error: ', error);
            throw error;
        }
    }


    async function createGradeLevelMapping() {
        const classSectionData = await fetchClassSectionData();
        const gradeLevelMapping = {};
        // Generate the mapping from class_section_data
        classSectionData.forEach(item => {
            gradeLevelMapping[item.section_name] = item.grade_level;
        });
    
        return gradeLevelMapping;
    }
   

    // Function to set the data-grade-level attribute
    // To be used as reference which options to hide and show
    async function setGradeLevelAttribute(idModal) {
        const gradeLevelMapping = await createGradeLevelMapping();
        console.log(gradeLevelMapping);
        // Iterate through the list and assign the 
        // value into data-grade-level attribute
        $(`${idModal} #id_class_section option`).each(function() {
            let classSectionName = $(this).val();
    
            if (gradeLevelMapping.hasOwnProperty(classSectionName)) {
                let gradeLevel = gradeLevelMapping[classSectionName];
                $(this).attr('data-grade-level', gradeLevel);
            }
            console.log('hello');
        });
    }


    // Function to initiate the modal form when modal is opened
    function initializeModal(idModal) {
        const gradeLevelField = `${idModal} #id_grade_level`;
        const classSectionField = `${idModal} #id_class_section`;
        // Add an empty selection to add student modal form
        $(classSectionField).prepend('<option value="" selected>Select Section</option>');
        
        // Call the function to set the data-grade-level attribute
        setGradeLevelAttribute(idModal);
        
        // Listen for changes in the grade_level field
        $(gradeLevelField).change(function() {
            // Reset the select field within the current modal
            $(`${idModal} #id_class_section`).val('');
            updateSectionOptions(gradeLevelField, classSectionField);
        });

        // Update the options when the modal is opened
        $(idModal).on('shown.bs.modal', function () {
            updateSectionOptions(gradeLevelField, classSectionField);
        });

        updateSectionOptions(gradeLevelField, classSectionField);
    };


    initializeModal('#addStudentModal');
    initializeModal('#register-form');
});
