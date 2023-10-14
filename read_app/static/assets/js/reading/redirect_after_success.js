$(document).ready(function() {
    $(document).on('htmx:afterRequest', function(evt) {
        let xhr = evt.detail.xhr;
        console.log(xhr)

        if (xhr.status === 200) {
            let response = JSON.parse(xhr.response);
            if (response.success === true) {
                console.log('Success');
                window.location.href = '/reading_material';
            }
        }
    })
});