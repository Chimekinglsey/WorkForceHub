$(document).ready(function () {
    function closeFlash() {
        let flashContainer = $(".flash-container");
        // Check if flashContainer is displayed as block
        if (flashContainer.css('display') === 'block') {
            setTimeout(function() {
                flashContainer.fadeOut(300);
            }, 5000);
        }
    }
    closeFlash();
});
