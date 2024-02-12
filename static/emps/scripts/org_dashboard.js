$(document).ready(function() {
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
                $('.spinner-container').hide();
                
                $('.backdrop').hide();
                form.trigger('reset');
                form.hide()
                $('#successModal').show()
                $('.create-org').show();

                // reload the page
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

        

        // Show modal when createOrgBtn is clicked
        $('.createOrgBtn').click(function() {
            showOrgModal();
        });
        $('.createBranchBtn').click(function() {
            showBranchModal();
        });



        // Hide modal when close button is clicked
        $('.close').click(function() {
            hideBranchModal();
            hideOrgModal();
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
        $(window).click(function(event) {
            // Check if .showBranches is currently displayed
            if ($('.showBranches').is(':visible')) {
                $('.showBranches').hide();
            }
        });
    });