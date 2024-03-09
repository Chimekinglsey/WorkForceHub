$(document).ready(function() {
    // TODO: Write a single function that performs ajax for all the modals (take all variables as arguments)

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
            url: '/orgDashboard/',
            method: 'POST',
            data: formData,
            success: function(response) {
                // Handle success response, e.g., redirect to branch creation
                $('.spinner-container').hide();
                form.trigger('reset');
                // reload the page
                window.location.href = '/orgDashboard/';
            },
            error: function(xhr, status, error) {
                // Handle error response
                $('.spinner-container').hide();
                $('#ErrorModal').show()
                console.error(error);
            }
        });
    });

        if ($(window).outerWidth() <= 768) {
            $('.ToggleContainer').show();
        } else {
            $('.ToggleContainer').hide();
        }
    // if outerWidth is <= 900px, toggle left pane down content when .ToggleContainer is clicked or hovered
    const toggleContainer = $('.ToggleContainer');

    toggleContainer.click(function() {
        if ($(window).outerWidth() <= 768) {
            $(this).toggleClass('active');
            $('.actionContainer').slideToggle();
        }
    });


    // if outerWidth is less <=900px add class active to .downMore, else remove class active. Bind it to window resize
    $(window).resize(function() {
        toggleDownMore();
    });
    function toggleDownMore() {
        if ($(window).outerWidth() <= 768) {
            $('.ToggleContainer').show();
        } else {
            $('.ToggleContainer').hide();
        }
    }

    toggleDownMore();
    // prefill the url in orgaization form
    $('.presignedUrl').on('input', function() {
        var val = $(this).val();
        var placeholder = $(this).attr('placeholder');
        if (val && val.startsWith(placeholder)) {
            var parts = val.split('/yourpage');
            if (parts.length > 1) {
                $(this).val(parts[0] + '/yourpage' + parts[1]);
            }
        }
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
                window.location.href = '/orgDashboard/';
            },
            error: function(xhr, status, error) {
                // Handle error response
                $('.spinner-container').hide();
                form.hide()
                $('.backdrop').hide();
                $('#ErrorModal').show()
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
                window.location.href = '/orgDashboard/';
            },
            error: function(xhr, status, error) {
                // Handle error response
                $('.spinner-container').hide();
                form.hide()
                $('.backdrop').hide();
                $('#ErrorModal').show()
                console.error(error);
            }
        });
    });

    $('#reset_delegate_password').submit(function(e) {
        // start spinner
        e.preventDefault();
        $('.spinner-container').show();

        // Serialize form data
        let formData = $(this).serialize();
        let form = $(this);

        // Send AJAX request to create organization
        $.ajax({
            url: '/resetDelegatePassword/',
            method: 'POST',
            data: formData,
            success: function(response) {
                // Handle success response, e.g., redirect to branch creation
                form.trigger('reset');
                window.location.href = '/orgDashboard/';
            },
            error: function(xhr, status, error) {
                // Handle error response
                $('.spinner-container').hide();
                form.hide()
                $('.backdrop').hide();
                $('#ErrorModal').show()
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
            $('#delegate-admin-form').show(); //change_admin_password_form
        }
        function showDelegatePasswordModal() {
            $('.create-org').hide();
            $('.backdrop').show();
            $('#reset_delegate_password').show();
        }
        function showDeleteOrg() {
            $('.backdrop').show();
            $('#deleteOrgModal').show();
        }
        // function to show change_admin_password_form when changeAdminPasswordBtn is clicked
        // function showChangeAdminPasswordModal() {
        //     $('.backdrop').show();
        //     $('#update_admin_password_form').show();
        // }

        // // hide update_admin_password_form
        // function hideChangeAdminPasswordModal() {
        //     $('.backdrop').hide();
        //     $('#update_admin_password_form').hide();
        // }



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
        function hideDelegatePasswordModal() {
            $('.backdrop').hide();
            $('#reset_delegate_password').hide();
            $('.create-org').show();
        }
        function hideDeleteOrg() {
            $('.backdrop').hide();
            $('#deleteOrgModal').hide();
        }
        function hideProfileUpdate() {
            $('.backdrop').hide();
            $('#profileUpdateForm').hide();
        }


        // Ensure passwords match before submission

        $('#password, #confirm_password').on('keyup', function () {
            let password = $('#password').val();
            let confirmPassword = $('#confirm_password').val();
    
            // Check if password and confirm password match
            if (password == confirmPassword) {
                $('#resetDelegateBtn').addClass('valid');
            } else {
                $('#resetDelegateBtn').removeClass('valid');
            }
        });


        $('#id_password1, #id_password2').on('keyup', function () {
            let password = $('#id_password1').val();
            let confirmPassword = $(' #id_password2').val();
    
            // Check if password and confirm password match
            if (password == confirmPassword) {
                $('.validateSmt').addClass('valid');
            } else {
                $('.validateSmt').removeClass('valid');
            }
        });

        // validate email for delegate creation form:
        $('input#id_email').on('blur', function() {
            let email = $(this).val();
            if (email.length < 8 || !email.includes('@') || !email.includes('.')){
               alert('Please enter a valid email')
            }
        });


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
        $('.resetDelegatePwdBtn').click(function() {
            showDelegatePasswordModal();
        });


        // update admin profile
        $('#updateProfileBtn').click(function(){
            $('.create-org').hide();
            $('.backdrop').show();
            $('#profileUpdateForm').show()
        })

        $('#profileUpdateForm').submit(function (){
            $('.spinner-container').show();
        })



        // Hide modal when close button is clicked
        $('.close').click(function() {
            $('.modal').hide(); 
            $('.backdrop').show();
            hideBranchModal();
            hideOrgModal();
            hideDelegateModal();
            hideDelegatePasswordModal();
            hideDeleteOrg();
            hideProfileUpdate()
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

        // display toggles for the different management options
        $('#transfers').click(function() {
            $('.mgt2').removeClass('active');
            let content = $(this).data('content');
            $(`.${content}`).addClass('active');
        });
        $('#reports').click(function() {
            let content = $(this).data('content');
            $('.mgt2').removeClass('active');
            $(`.${content}`).addClass('active');
        });

        $('.manageBranch').click(function() {
            let content = $(this).data('content');
            $('.mgt2').removeClass('active');
            $(`.${content}`).addClass('active');
        });

        $('.delegateBtn').click(function() {
            let content = $(this).data('content');
            $('.mgt2').removeClass('active');
            $(`.${content}`).addClass('active');
        });

        $('.superuserBtn').click(function() {
            let content = $(this).data('content');
            $('.mgt2').removeClass('active');
            $(`.${content}`).addClass('active');
        });

        $('.adminSettings').click(function() {
            let content = $(this).data('content');
            $('.mgt2').removeClass('active');
            $(`.${content}`).addClass('active');
        });

        // Accept or decline  transfers
        $('.approve-transfer-btn').click(function() {
            let transferId = $(this).data('transferid');
            $.post(`/manageTransferRequest/${transferId}/`, { action: 'accept' }, function(data) {
                if (data.error) {
                    flashMessage(data.error);
                }
                window.location.reload()
            });
        });
    
        $('.decline-transfer-btn').click(function() {
            let transferId = $(this).data('transferid');
            $.post(`/manageTransferRequest/${transferId}/`, { action: 'decline' }, function(data) {
                // Handle success or error response from the server
                if (data.error) {
                    flashMessage(data.error);
                }
                window.location.reload()
                message = "Success"
                flashMessage(message);
    
             });
        });
        
        // Open the modal
        function openModal(modalId) {
            $(`#${modalId}`).css("display", "block");
        }
        
        // Close the modal
        function closeModal() {
            $('.backdrop').hide();
            $(".modal").css("display", "none");
        }
        
        // When the user clicks on the close button or cancel button, close the modal
        $(".cancelConfirmBtn").click(function() {
            $('.backdrop').show();
            closeModal();
        });


        /* Functions for branch, delegate and admin management/operations
            (Remember to make this a single function that takes parameters instead of duplications)
        */

        // delete delegate
        $('.deleteDelegateBtn').click(function(){
            let admin_id = $(this).data('delegateid')
            openModal('deleteDelegateModal')
            $('.proceedDeleteBtn').click(function(){
                $.post(`/org/deleteDelegate/${delegate_id}/`,function(data) {
                    // Handle success or error response from the server
                    if (data.error) {
                        flashMessage(data.error);
                    }
                    window.location.reload()
                    message = "Success"
                    flashMessage(message);
                 });
            });
            $('.cancelDeleteBtn').click(function(){
                closeModal()
            })
        })

        // delete branch
        $('.deleteBranchBtn').click(function(){
            let branch_id = $(this).data('branchid')
            openModal('deleteBranchModal')
            $('.proceedDeleteBtn').click(function(){
                $.post(`/org/deleteBranch/${branch_id}/`,function(data) {
                    // Handle success or error response from the server
                    if (data.error) {
                        flashMessage(data.error);
                    }
                    window.location.reload()
                    message = "Success"
                    flashMessage(message);
                 });
            });
            $('.cancelDeleteBtn').click(function(){
                closeModal()
            })
        })

        // delete organization
        $('#deleteOrgBtn').click(function(){
            let org_id = $(this).data('orgid');
            openModal('deleteOrgModal');
            
            // listen for input events on the deleteOrgInput field
            $('#deleteOrgInput').on('input', function(){
                // check if the input value is exactly equal to 'Permanent Delete Organization'
                let input = $(this).val(); 
                if (input === 'Permanently Delete Organization') {
                    $('#confirmOrgDeleteBtn').addClass('valid'); 
                } else {
                    $('#confirmOrgDeleteBtn').removeClass('valid'); 
                }
            });

            $('#confirmOrgDeleteBtn').click(function(){
                $.post(`/org/deleteOrg/${org_id}/`, function(data) {
                    window.location.reload();
                });
            });

            // handle click event on the cancel delete button
            $('.cancelDeleteBtn').click(function(){
                closeModal();
            });
        });


        // suspend delegate
        $('.suspendDelegateBtn').click(function(){
            let delegate_id = $(this).data('delegateid')
            openModal('suspendDelegateModal')
            $('.proceedDeleteBtn').click(function(){
                $.post(`/org/suspendDelegate/${delegate_id}/`,function(data) {
                    // Handle success or error response from the server
                    if (data.error) {
                        flashMessage(data.error);
                    }
                    window.location.reload()
                    message = "Success"
                    flashMessage(message);
                 });
            });
            $('.cancelDeleteBtn').click(function(){
                closeModal()
            })
        })
        
        // Activate suspended delegate
        $('.activateDelegateBtn').click(function(){
            let delegate_id = $(this).data('delegateid')
            openModal('activateDelegateModal')
            $('.proceedDeleteBtn').click(function(){
                $.post(`/org/activateDelegate/${delegate_id}/`,function(data) {
                    // Handle success or error response from the server
                    if (data.error) {
                        flashMessage(data.error);
                    }
                    window.location.reload()
                    message = "Success"
                    flashMessage(message);
                 });
            });
            $('.cancelDeleteBtn').click(function(){
                closeModal()
            })
        })

        // promote delegate to organization admin
        $('.promoteDelegateBtn').click(function(){
            let delegate_id = $(this).data('delegateid')
            openModal('promoteDelegateModal')
            $('.proceedDeleteBtn').click(function(){
                $.post(`/org/promoteDelegate/${delegate_id}/`,function(data) {
                    // Handle success or error response from the server
                    if (data.error) {
                        flashMessage(data.error);
                    }
                    window.location.reload()
                    message = "Success"
                    flashMessage(message);
                 });
            });
            $('.cancelDeleteBtn').click(function(){
                closeModal()
            })
        })

        // demote admin to delegate
        $('.demoteAdminBtn').click(function(){
            let delegate_id = $(this).data('delegateid')
            openModal('demoteAdminModal')
            $('.proceedDeleteBtn').click(function(){
                $.post(`/org/demoteAdmin/${delegate_id}/`,function(data) {
                    // Handle success or error response from the server
                    if (data.error) {
                        flashMessage(data.error);
                    }
                    window.location.reload()
                    message = "Success"
                    flashMessage(message);
                 });
            });
            $('.cancelDeleteBtn').click(function(){
                closeModal()
            })
        })

        // suspend admin
        $('.suspendAdminBtn').click(function(){
            let admin_id = $(this).data('delegateid')
            openModal('suspendAdminModal')
            $('.proceedDeleteBtn').click(function(){
                $.post(`/org/suspendAdmin/${admin_id}/`,function(data) {
                    // Handle success or error response from the server
                    if (data.error) {
                        flashMessage(data.error);
                    }
                    window.location.reload()
                    message = "Success"
                    flashMessage(message);
                 });
            });
            $('.cancelDeleteBtn').click(function(){
                closeModal()
            })
        })

        // Activate suspended admin
        $('.activateAdminBtn').click(function(){
            let admin_id = $(this).data('delegateid')
            openModal('activateAdminModal')
            $('.proceedDeleteBtn').click(function(){
                $.post(`/org/activateAdmin/${admin_id}/`,function(data) {
                    // Handle success or error response from the server
                    if (data.error) {
                        flashMessage(data.error);
                    }
                    window.location.reload()
                    message = "Success"
                    flashMessage(message);
                 });
            });
            $('.cancelDeleteBtn').click(function(){
                closeModal()
            })
        })

        // show filter when updateOrgBtn is clicked and close when close is clicked
        $('#updateOrgBtn').click(function(){
            $('#orgSubmitBtn').text('Update')
            $('.backdrop').show();
            $('.create-org').hide();
        });

//   modify dropdown

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
            if ($(window).outerWidth() > 768) {
                updateLeftPanePosition();
            }
        });
    
        // Initial position update
        if ($(window).outerWidth() > 768){
            updateLeftPanePosition();
        }
    });
