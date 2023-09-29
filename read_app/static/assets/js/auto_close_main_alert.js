document.addEventListener('DOMContentLoaded', function() {
    let alertDurationMilliseconds = 5000;

    // Automatically close the alert 
    setTimeout(function() {
        let alert = document.getElementById('alert');
        alert.classList.remove('show');
    }, alertDurationMilliseconds); 
});