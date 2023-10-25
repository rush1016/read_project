let questionLimit = 1;

function updateSaveButton(formCount) {
    const saveButton = $('#submit-all');
    let formCount = $("#question-container form").length;

    if (formCount == questionLimit) {
        saveButton.removeClass('d-none');
    }
    else if (!saveButton.hasClass('d-none') && formCount < questionLimit) {
        saveButton.addClass('d-none');
    }
};

updateSaveButton(formCount);