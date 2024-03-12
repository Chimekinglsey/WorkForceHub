$(document).ready(function() {

// Validator for images
    $('#id_profile_picture, #profilePictureEdit').change(function() {
        let id = $(this)
        let fileName = id.val();
        let validExtensions = ['jpeg', 'jpg', 'JPEG', 'JPG', 'PNG', 'png'];
        let fileExtension = fileName.split('.').pop().toLowerCase();
        
        if ($.inArray(fileExtension, validExtensions) == -1) {
            alert('Please select a valid image file (JPEG, JPG, PNG)');
            id.val('');
            return false;
        }
    });

    $('#homeLink').click(function(){
        window.location.href = '/';
    })
    $('input[type="search"]').attr('placeholder', 'Enter search text');


    $('#menu-toggle').click(function() {
        $('.header-nav').slideToggle()
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
        "info": false, // Hide information display
    });

    

    // Use forms back button
    $('.backBtn').on('click', function() {
        window.history.back();
    });

});
