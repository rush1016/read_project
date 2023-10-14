$(document).ready(function() {
    let confirmDeletePassageButton = $('#confirm-delete-passage-button');
    let passageId = $('#passage-id').val();

    confirmDeletePassageButton.click(function() {
        $.ajax({
            type: 'POST',
            url: 'delete_passage' + passageId
        })
    })
});