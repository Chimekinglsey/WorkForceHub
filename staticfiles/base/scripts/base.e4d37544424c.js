$(document).ready(function() {
    $('#homeLink').click(function(){
        window.location.href = '/';
    })
    $('input[type="search"]').attr('placeholder', 'Enter search text');


    $('#menu-toggle').click(function() {
        $('.header-nav').toggleClass('show');
    });

    // Close the menu when clicking outside of it
    $(document).click(function(event) {
        let nav = $('.header-nav');
        let menuToggle = $('#menu-toggle');
        if (!nav.is(event.target) && !menuToggle.is(event.target) && nav.has(event.target).length === 0) {
            nav.removeClass('show');
        }
    });
    
    // Pagination dataTable
    let table = $('.dataTable').DataTable({
        "paging": true,
        "searching": true, // Disable DataTables search to use custom search
        "info": true // Hide information display
    });

    // Use forms back button
    $('.backBtn').on('click', function() {
        window.history.back();
    });

});
