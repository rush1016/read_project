$(document).ready(function() {
    // Buttons
    let startReadingButton = $('#start-reading-button');
    let startAnswerButton = $('#start-answering');

    // Containers
    let instructionCard = $('#instruction-card');
    let assessmentContainer = $('#assessment-container');
    let questionContainer = $('#question-container');
    let passageContainer = $('#passage-container');
    let passageBox = $('#passage-box');
    let passageBoxButton = $('#passage-box-button');
    
    // Timer
    let timerInterval;
    let timerIntervalExtra;
    let readingTime = 0;
    let answeringTime = 0;
    let modalOpened = 0;
    let totalExtra = 0;
    let extraReadingTime = 0;
        

    startReadingButton.click(function() {
        assessmentContainer.removeClass('d-none');
        instructionCard.remove();
        // Start the reading timer as soon as the page loads
        clearInterval(timerInterval);
        timerInterval = setInterval(function () {
            readingTime++;
            $('#reading-time').val(readingTime);
        }, 1000);
    });


    startAnswerButton.click(function() {
        questionContainer.removeClass('d-none')
        passageContainer.remove()
        passageBox.removeClass('d-none')
        passageBoxButton.removeClass('d-none')
        $(this).remove()
        clearInterval(timerInterval);
        timerInterval = setInterval(function () {
            answeringTime++;
            $('#answering-time').val(answeringTime);
        }, 1000);
    });
    
    $('#modal-passage-box').on('show.bs.modal', function() {
        clearInterval(timerIntervalExtra);
        timerIntervalExtra = setInterval(function () {
            extraReadingTime++;
        }, 1000);

        totalExtra += extraReadingTime;
        extraReadingTime = 0;
        

        modalOpened += 1;
        $('#extra-reading-time').val(totalExtra);
        $('#review-count').val(modalOpened);
        console.log('modalOpened: ', modalOpened);
        console.log('totalReading: ', $('#reading-time').val());
        console.log('totalextra: ', totalExtra);
;
    })

    $('#assessment-form').on('submit', function () {
        clearInterval(timerInterval);
    });
});
