$(document).ready(function() {
    let totalQuestions = $('#question-count').val();
    let correctAnswers = $('#student-score').val();
    let wrongAnswers = totalQuestions-correctAnswers;

    let ctx = $('#donutChart')[0].getContext('2d');

    let data = {
        labels: ['Correct', 'Wrong'],
        datasets: [{
            data: [correctAnswers, wrongAnswers], // The values you want to display
            backgroundColor: ['#03ff31', '#ed0c0c'], // Colors for each value
        }]
    };

    // Create a donut chart
    let donutChart = new Chart(ctx, {
        type: 'doughnut',
        data: data,
    });
});