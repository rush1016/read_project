$(document).ready(function () {
    $('#interactive-area').on('click', '.word', function (event) {
        setTimeout(function () {
            showContextMenu(event, $(event.target));
        }, 10);
        getMiscues()    
    });

    $(document).on('click', function () {
        $('.context-menu').remove();
    });
    getMiscues()    
});

function showContextMenu(event, clickedElement) {
    const existingMiscue = clickedElement.data('miscue');

    if (existingMiscue) {
        showContextMenuForExistingMiscue(event, clickedElement);
    } else {
        clickedElement.addClass('bg-warning');

        const contextMenu = $('<div>').addClass('context-menu border border-dark')
            .append(
                '<ul class="list-group">' +
                '<li class="list-group-item clickable-item" data-action="Mispronunciation">Mispronunciation</li>' +
                '<li class="list-group-item clickable-item" data-action="Omission">Omission</li>' +
                '<li class="list-group-item clickable-item" data-action="Substitution">Substitution</li>' +
                '<li class="list-group-item clickable-item" data-action="Insertion">Insertion</li>' +
                '<li class="list-group-item clickable-item" data-action="Repetition">Repetition</li>' +
                '<li class="list-group-item clickable-item" data-action="Transposition">Transposition</li>' +
                '<li class="list-group-item clickable-item" data-action="Reversal">Reversal</li>' +
                '<li class="list-group-item clickable-item" data-action="Self-correction">Self-correction</li>' +
                '</ul>'
            );

        contextMenu.css({
            position: 'absolute',
            left: event.pageX + 'px',
            top: event.pageY + 'px'
        });

        $('body').append(contextMenu);

        $('.clickable-item').on('click', function () {
            handleItemClick($(this).data('action'), clickedElement.text(), clickedElement.data('index'));
            $('.context-menu').remove();
        });

        event.preventDefault();
    }
}


function showContextMenuForExistingMiscue(event, clickedElement) {
    clickedElement.addClass('bg-warning');

    const contextMenu = $('<div>').addClass('context-menu border border-dark')
        .append(
            '<ul class="list-group">' +
            '<li class="list-group-item clickable-item" data-action="Delete">Delete</li>' +
            '</ul>'
        );

    contextMenu.css({
        position: 'absolute',
        left: event.pageX + 'px',
        top: event.pageY + 'px'
    });

    $('body').append(contextMenu);

    $('.clickable-item').on('click', function () {
        if ($(this).data('action') === 'Delete') {
            handleDeleteMiscue(clickedElement);
        }
        $('.context-menu').remove();
    });

    event.preventDefault();
}


function handleItemClick(action, word, index) {
    console.log('Clicked item: ' + action + ' for word: ' + word);
    let passageId = $('#passage-id').val()
    let assessmentId = $('#assessment-id').val()

    const csrfToken = getCookie('csrftoken');

    $.ajax({
        url: '../miscue/save',
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        data: {
            'word': word,
            'miscue': action,
            'index': index,
            'passage_id': passageId,
            'assessment_id': assessmentId
        },
        success: function (response) {
            getMiscues();
        },
        error: function (error) {
            console.error('Error saving data:', error);
        }
    });
}


function handleDeleteMiscue(clickedElement) {
    let passageId = $('#passage-id').val();
    let assessmentId = $('#assessment-id').val();

    const csrfToken = getCookie('csrftoken');

    $.ajax({
        url: '../miscue/delete',
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        data: {
            'word': clickedElement.text(),
            'index': clickedElement.data('index'),
            'passage_id': passageId,
            'assessment_id': assessmentId
        },
        success: function (response) {
            clickedElement.removeClass('bg-warning');
            clickedElement.removeAttr('data-miscue');
            getMiscues();
        },
        error: function (error) {
            console.error('Error deleting data:', error);
        }
    });
}


function getMiscues() {
    let assessmentId = $('#assessment-id').val();
    const csrfToken = getCookie('csrftoken');

    $.ajax({
        url: '../miscue/get',
        type: 'GET',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        data: {
            'assessment_id': assessmentId,
        },
        success: function (data) {
            renderInteractiveArea(data);
        },
        error: function (error) {
            console.error('Error loading data:', error);
        }
    })
}


function renderInteractiveArea(data) {
    // Assuming data.words is the list of all words
    // and data.words_with_miscues is the list of words with miscues
    let $interactiveArea = $('#interactive-area');
    
    // Clear existing content
    $interactiveArea.find('.display-5').empty();
    let i = 1;
    // Render all words
    data.words.forEach(function (word) {
        $interactiveArea.find('.display-5').append(`<span class="word" data-index="${i}">${word} </span>`);
        i++;
    });


    // Apply miscues
    data.miscues.forEach(function (miscue) {
        let $wordElements = $interactiveArea.find(`.word[data-index="${miscue.index}"]:contains('${miscue.word}')`);
        $wordElements.addClass('bg-warning');
        $wordElements.attr('data-miscue', miscue.miscue);
    });
}


// Function to get the CSRF token from the cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if the cookie name matches the desired name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}