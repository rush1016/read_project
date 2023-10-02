$(document).ready(function() {
    let alertDurationMilliseconds = 5000;

    // Automatically close the alert 
    setTimeout(function() {
        let alert = $('#alert');
        alert.removeClass('show');
    }, alertDurationMilliseconds); 
});
