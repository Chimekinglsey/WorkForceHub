$(document).ready(function() {
    $('#menu-toggle').click(function() {
        $('nav').toggleClass('show');
    });

    // Close the menu when clicking outside of it
    $(document).click(function(event) {
        let nav = $('.header-nav');
        let menuToggle = $('#menu-toggle');
        if (!nav.is(event.target) && !menuToggle.is(event.target) && nav.has(event.target).length === 0) {
            nav.removeClass('show');
        }
    });

});
