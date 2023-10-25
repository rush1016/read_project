$(document).ready(function() {
    let questionForm = $('.question-form');
    let questionFormset = $('.question-form:first').clone();
    let totalForms = $('#id_question_set-TOTAL_FORMS');
    let addQuestionButton = $('#add-question-button');
    let formsetCount = totalForms.val();

    addQuestionButton.click(function() {
        let newFormset = questionFormset.clone()
        newFormset.find('input, textarea').each(function(){
            let oldName = $(this).attr('name');
            let newName = oldName.replace('question_set-0-', 'question_set-' + (formsetCount) + '-');
            // Replace the name and id prefixes to identify each set of question and choices
            $(this).attr('name', newName);
            $(this).attr('id', newName);
        });
            
        formsetCount++;  
        questionForm.append(newFormset);
        totalForms.val(formsetCount);
    });

});