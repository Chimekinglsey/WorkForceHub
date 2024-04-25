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


    $('#menu-toggle').click(function(e) {
        e.stopPropagation();
        $('.header-nav').slideToggle()
    });


    // Close the menu when clicking outside of it
    //  apply this only when screen size is less than 900px. Attach this to resize and 
    $(document).click(function(event) {
            if ($(window).outerWidth() <= 900) {
            let nav = $('.header-nav');
            let menuToggle = $('#menu-toggle');
            if (!nav.is(event.target) && !menuToggle.is(event.target) && nav.has(event.target).length === 0) {
                nav.slideUp();
                }
            }
        });
    $(window).resize(function () {
        if ($(window).outerWidth() > 900) {
            $('.header-nav').css('display', 'flex');
        }
    })
    
    
    // Pagination dataTable
    let table = $('.dataTable').DataTable({
        "paging": true,
        "searching": true, // Disable DataTables search to use custom search
        "info": true, // Show information display(1 of 10 out of nth entries)
    });

    

    // Use forms back button
    $('.backBtn').on('click', function() {
        window.history.back();
    });

        // Calculate the minimum and maximum date
        let minDate = new Date();
        minDate.setFullYear(minDate.getFullYear() - 150); // 150 years ago
        let maxDate = new Date();
        maxDate.setFullYear(maxDate.getFullYear() - 12); // 12 years ago
    
        // Format min and max date as YYYY-MM-DD
        let minDateString = formatDate(minDate);
        let maxDateString = formatDate(maxDate);
    
        // Set min and max attributes for input with id 'dob' (for date of birth)
        $('#dob').attr('min', minDateString);
        $('#dob').attr('max', maxDateString);
    
        // Set min and max attributes for input with id 'id_dob' (for date of birth in django form)
        $('#id_dob').attr('min', minDateString);
        $('#id_dob').attr('max', maxDateString);
    
    // Function to format date as YYYY-MM-DD
    function formatDate(date) {
        var year = date.getFullYear();
        var month = ('0' + (date.getMonth() + 1)).slice(-2);
        var day = ('0' + date.getDate()).slice(-2);
        return year + '-' + month + '-' + day;
    }
    
});
