$(document).ready(function() {
    // Buttons
    let startReadingButton = $('#start-reading-button')
    let startAnswerButton = $('#start-answering');

    // Containers
    let instructionCard = $('#instruction-card')
    let assessmentContainer = $('#assessment-container')
    let questionContainer = $('#question-container');

    // Timer
    let timer = $('#timer')
    let timerInterval;
    let readingTime = 0;
    let answeringTime = 0;
        

    // Function to update the timer display
    function updateTimerDisplay(time) {
        let minutes = Math.floor(time / 60);
        let seconds = time % 60;
        timer.text(minutes + ':' + (seconds < 10 ? '0' : '') + seconds);
    }


    startReadingButton.click(function() {
        assessmentContainer.removeClass('d-none')
        instructionCard.remove()
        // Start the reading timer as soon as the page loads
        clearInterval(timerInterval);
        timerInterval = setInterval(function () {
            readingTime++;
            $('#reading-time').val(readingTime);
            updateTimerDisplay(readingTime);
        }, 1000);
    })


    startAnswerButton.click(function() {
        questionContainer.removeClass('d-none')
        $(this).remove()
        clearInterval(timerInterval);
        timerInterval = setInterval(function () {
            answeringTime++;
            $('#answering-time').val(answeringTime);
            updateTimerDisplay(answeringTime);
        }, 1000);
    })
    

    $('#assessment-form').on('submit', function () {
        clearInterval(timerInterval);
    });
});
