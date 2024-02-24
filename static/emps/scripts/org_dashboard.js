$(document).ready(function() {
    // Function to update the left pane's position

    // close modal button
    $('.closeModal').click(function() {
        $('.modal').hide();
    });

    //  Ajax to create organization
    $('#organization-form').submit(function(e) {
        // start spinner
        e.preventDefault();
        $('.spinner-container').show();
        // Perform form validation here if needed - None for now

        // Serialize form data
        let formData = $(this).serialize();
        let form = $(this);

        // Send AJAX request to create organization
        $.ajax({
            url: '/createOrg/',
            method: 'POST',
            data: formData,
            success: function(response) {
                // Handle success response, e.g., redirect to branch creation
                $('.spinner-container').hide();
                form.trigger('reset');
                // reload the page
                window.location.href = '/createOrg/';
            },
            error: function(xhr, status, error) {
                // Handle error response
                $('.spinner-container').hide();
                $('#ErrorModal').show()
                console.error(error);
            }
        });
    });



    $('#branch-form').submit(function(e) {
        // start spinner
        e.preventDefault();
        $('.spinner-container').show();
        // Perform form validation here if needed - None for now

        // Serialize form data
        let formData = $(this).serialize();
        let form = $(this);

        // Send AJAX request to create organization
        $.ajax({
            url: '/org/createBranch/',
            method: 'POST',
            data: formData,
            success: function(response) {
                // Handle success response, e.g., redirect to branch creation
                form.trigger('reset');
                // reload the page
                window.location.href = '/createOrg/';
            },
            error: function(xhr, status, error) {
                // Handle error response
                $('.spinner-container').hide();
                form.hide()
                $('.backdrop').hide();
                $('#ErrorModal').show()
                $('.create-org').show();
                console.error(error);
            }
        });
    });


    $('#delegate-admin-form').submit(function(e) {
        // start spinner
        e.preventDefault();
        $('.spinner-container').show();

        // Serialize form data
        let formData = $(this).serialize();
        let form = $(this);

        // Send AJAX request to create organization
        $.ajax({
            url: '/org/createDelegate/',
            method: 'POST',
            data: formData,
            success: function(response) {
                // Handle success response, e.g., redirect to branch creation
                form.trigger('reset');
                // reload the page
                window.location.href = '/createOrg/';
            },
            error: function(xhr, status, error) {
                // Handle error response
                $('.spinner-container').hide();
                form.hide()
                $('.backdrop').hide();
                $('#ErrorModal').show()
                $('.create-org').show();
                console.error(error);
            }
        });
    });

        // Function to show organization form and backdrop
        function showOrgModal() {
            $('.create-org').hide();
            $('#organization-form').show();
            $('.backdrop').show();
        }
        function showBranchModal() {
            $('.create-org').hide();
            $('#branch-form').show();
            $('.backdrop').show();
        }
        function showDelegateModal() {
            $('.create-org').hide();
            $('.backdrop').show();
            $('#delegate-admin-form').show();
        }


        // Function to hide the form and backdrop
        function hideOrgModal() {
            $('.backdrop').hide();
            $('#organization-form').hide();
            $('.create-org').show();
        }

        function hideBranchModal() {
            $('.backdrop').hide();
            $('#branch-form').hide();
            $('.create-org').show();
        }
        function hideDelegateModal() {
            $('.backdrop').hide();
            $('#delegate-admin-form').hide();
            $('.create-org').show();
        }


        

        // Show modal when createOrgBtn is clicked
        $('.createOrgBtn').click(function() {
            showOrgModal();
        });
        $('.createBranchBtn').click(function() {
            showBranchModal();
        });
        $('.createDelegateBtn').click(function() {
            showDelegateModal();
        });




        // Hide modal when close button is clicked
        $('.close').click(function() {
            hideBranchModal();
            hideOrgModal();
            hideDelegateModal();
        });
    
        $('.listBranches').click(function(event){
            // Prevent the click event from propagating to the document
            event.stopPropagation();
            if ($('.showBranches').is(':visible')) {
                $('.showBranches').hide();
            } else {
                $('.showBranches').show();
            }
        });
        // listDelegates
        $('.listDelegates').click(function(event){
            // Prevent the click event from propagating to the document
            event.stopPropagation();
            if ($('.showDelegates').is(':visible')) {
                $('.showDelegates').hide();
            } else {
                $('.showDelegates').show();
            }
        });
        $(window).click(function(event) {
            // Check if .showBranches is currently displayed
            if ($('.showBranches').is(':visible')) {
                $('.showBranches').hide();
            }
            if ($('.showDelegates').is(':visible')) {
                $('.showDelegates').hide();
            }
        });
    });
    
    //   updateLeftPanePosition();
    $(document).ready(function() {
        // Function to update left pane position
        function updateLeftPanePosition() {
            let headerHeight = $('.header').outerHeight();
            let footerHeight = $('.footer').outerHeight();
            let leftPane = $('.left-pane-org');
            let scrollTop = $(window).scrollTop();
    
            // Calculate the desired top position for the left pane
            let desiredTop = 85.5 - scrollTop;
            if (desiredTop < 10) desiredTop = 10; // Minimum top position
            if (desiredTop + leftPane.outerHeight() > $(window).innerHeight() - footerHeight) {
                desiredTop = $(window).innerHeight() - footerHeight - leftPane.outerHeight();
            }
    
            // Update the left pane's top position
            leftPane.css('top', desiredTop + 'px');
        }
    
        // Update left pane position on window scroll and resize
        $(window).on('scroll resize', function() {
            updateLeftPanePosition();
        });
    
        // Initial position update
        updateLeftPanePosition();
    });
    