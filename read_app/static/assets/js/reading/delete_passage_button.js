$(document).ready(function() {
    let deletePassageButton = $('.delete-passage-button');
    let modal = $('#delete-passage-modal');

    deletePassageButton.click(function() {
        let passageId = $(this).data('passage-id');
        getPassageInfo(passageId)
        .then(function(passage_data) {
            let passageId = passage_data['passage_id']
            let passageTitle = passage_data['passage_title'];
            let passageGradeLevel = passage_data['grade_level'];
            let fieldContainer = $('#field-container');
            
            // Add information about the passage
            fieldContainer.append(`<h1 id="modal-passage-title">Title: ${passageTitle}</h1>`, `<h3 id="modal-passage-grade-level">Grade ${passageGradeLevel}</h3>`);
            fieldContainer.append(`<input type="hidden" id="passage-id" name="passage_id" value="${passageId}"`);
        })
        .catch(function(error) {
            console.error('Error:', error)
        })
    })

    // Clear the modal when closed
    modal.on('hidden.bs.modal', function (e) {
        // Clear the content inside the modal
        $('#modal-passage-title').remove();
        $('#modal-passage-grade-level').remove();
    });
});