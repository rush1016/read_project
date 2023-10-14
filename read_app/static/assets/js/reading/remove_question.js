$(document).ready(function(){
    $('.remove-form-button').click(function() {
        let formCount = $("#question-container form").length;
        updateSaveButton(formCount);
    })
});