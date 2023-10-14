$(document).ready(function() {
    function dismissMessages() {
        // Target messages with the custom CSS class applied by Django
        let messages = $(".dismissable-message");
        console.log(messages);

        // Automatically dismiss messages after 5 seconds
        for (let i = 0; i < messages.length; i++) {
            let message = messages.item(i);
            console.log(message);
            setTimeout(function () {
                message.hide();
            }, 5000); // 5000 milliseconds (5 seconds)
        };
    }
    dismissMessages();
});
