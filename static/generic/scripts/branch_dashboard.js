$(document).ready(function () {
    // flash messages
    // AJAX success callback function
function flashMessage(response) {
        if (response.type === 'success') {
            $('#messageBody').text(`Success:  ${response.message}`);
            $('.flash-ajax-message').addClass('success-message');
        } 
        else if (response.type === 'error') {
            $('#messageBody').text(`Error:  ${response.message}`);
            $('.flash-ajax-message').addClass('error-message');
        }
        else {
            $('#messageBody').text(response.slice(0, 50) + '...');
            $('.flash-ajax-message').addClass('error-message');
        }
     }

     $('.flash-close-btn').click(function() {
        $('.flash-ajax-message').removeClass('success-message');
        $('.flash-ajax-message').removeClass('error-message');
        $('.flash-ajax-message').hide();
        $('.backdrop').hide();
     });
     

    // Timeout to fade out flash message
    function timeoutFlashMessage() {
    setTimeout(function() {
        $('.flash-ajax-message').slideToggle(function() {
            $('.flash-ajax-message').removeClass('success-message');
            $('.flash-ajax-message').removeClass('error-message');
        });
    }, 5000); // 5 seconds
    }


    // Load content dynamically on link click
    $('.featuresItem').click(function () {
        content = $(this).data('content');
        $('.mgt').hide();
        $(`.${content}`).show();
    });
    // Function to toggle Feature list on heading click for screens less than 900px
    $('.featuresToggleContainer').click(function () {
        if ($(window).width() <= 754) {
            $('.featuresList').slideToggle();
        }
    });
    
    $('.featuresItem').click(function () {
            if ($(window).width() <= 754) {
                $('.featuresList').slideToggle();
            }
        });

        // Function to close Feature list when window is resized to larger than 900px
        $(window).resize(function () {
            if ($(window).width() > 754) {
                $('.featuresList').slideDown();
                $('.actions').slideDown();
                $('.featuresToggle').removeClass('shake');
                $('.left-pane').removeClass('shake-parent')
                $('.left-pane').on('mouseleave', function() {
                    $('.featuresList').slideDown();
                });
    
            }
            else {
                $('.featuresList').slideUp();
                $('.actions').slideUp();
                $('.featuresToggle').addClass('shake');
                $('.left-pane').addClass('shake-parent')
    
                $('.featuresToggleContainer').on('mouseenter click', function() {
                    $('.featuresList').slideDown();
                });
                $('.left-pane').on('mouseleave', function() {
                    $('.featuresList').slideUp();
                });
            }
        });
        


        // display leave requests when #payrollManagement is clicked

        // leave and employee management
        if ($(window).width() <= 754) {
            $(".actions").slideToggle();
            $(".featuresList").slideToggle(
            );
            $('.featuresToggle').addClass('shake');
            $('.left-pane').addClass('shake-parent')

            $('.featuresToggleContainer').on('mouseenter click', function() {
                $('.featuresList').slideDown();
            });
            $('.left-pane').on('mouseleave', function() {
                $('.featuresList').slideUp();
            });
        }
        else {
            $('.featuresToggle').removeClass('shake');
            $('.left-pane').removeClass('shake-parent')
        }
        // employee management tab
        $(".tab").on("click", function() {
            $(".tab").removeClass("active");
            $(this).addClass("active");
            let tab = $(this).data("tab");
            $(".tab-contents").hide();
            $(`#${tab}`).show();
        });

        // leave management tab
        $(".tab2").on("click", function() {
            $(".tab2").removeClass("active");
            $(this).addClass("active");
            let tab = $(this).data("tab2");
            $(".tab-contents2").hide();
            $(`#${tab}`).show();
        });

        // Payroll Management tab
        $(".tab3").on("click", function() {
            $(".tab3").removeClass("active");
            $(this).addClass("active");
            let tab = $(this).data("tab3");
            $(".tab-contents3").hide();
            $(`#${tab}`).show();
        });

        // Performance Management tab
        $(".tab4").on("click", function() {
            $(".tab4").removeClass("active");
            $(this).addClass("active");
            let tab = $(this).data("tab4");
            $(".tab-contents4").hide();
            $(`#${tab}`).show();
        });

        

        
    // Menu Toggle
        $(".menuToggle").on("click", function() {
            if ($(window).width() < 800) {
                $(".actions").slideToggle();
            }
        });

    // Leave Requests
        $("#searchLeaveHistory").on("keyup", function() {
            let value = $(this).val().toLowerCase();
            $(".leave-list tbody tr").filter(function() {
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
            });
        });

    // Employee Management
    $('.dropdown').on('click', function(event) {
        event.stopPropagation();
        $(this).find('.dropdown-menu').toggle();
    });

    $(document).on('click', function(event) {
        if (!$(event.target).closest('.dropdown').length) {
            $('.dropdown-menu').hide();
        }
    });


    $('.moreEmpDetail#viewEmpDetailBtn').click(function(e) {
        e.preventDefault();
        $('.backdrop').show();
        $('.spinner-container').show();
        let employeeId = $(this).data('employeeid');
        $.ajax({
            url: `/api/employees/${employeeId}/`,
            method: 'GET',
            dataType: 'json',
            success: function(response) {
                
                populateViewModal(response);    
            },
            error: function(xhr, status, error) {
                flashMessage(error);
                $('.flash-ajax-message').slideToggle(
                    timeoutFlashMessage()
                );
                console.error('Error fetching employee data:', error);
            }
        });
    });
        // Convert timestamp to YYYY-MM-DD HH:MM format
    function formatDateTime(timestamp) {
        if (!timestamp) {
            return '';
        }
        let date = new Date(timestamp);
        let year = date.getFullYear();
        let month = ('0' + (date.getMonth() + 1)).slice(-2);
        let day = ('0' + date.getDate()).slice(-2);
        let hours = ('0' + date.getHours()).slice(-2);
        let minutes = ('0' + date.getMinutes()).slice(-2);
        return `${year}-${month}-${day} @ ${hours}:${minutes}`;
    }


    function populateViewModal(employeeData) {
        // populate profile picture
        $('#profilePictureView').attr('src', employeeData.profile_picture);
        // Populate personal details
        $('#empFullNameView').text(`${employeeData.first_name} ${employeeData.middle_name[0].toUpperCase()}. ${employeeData.last_name}`);
        $('#emailView').text(employeeData.email);
        $('#phone_numberView').text(employeeData.phone_number);
        $('#dobView').text(employeeData.dob);
        $('#genderView').text(employeeData.gender);
        $('#marital_statusView').text(employeeData.marital_status);
        $('#addressView').text(employeeData.address);
        $('#nationalityView').text(employeeData.nationality);
        $('#state_of_originView').text(employeeData.state_of_origin);

        // Populate bank details
        $('#bankNameView').text(employeeData.bank_name);
        $('#accountNumberView').text(employeeData.account_number);
        $('#accountNameView').text(employeeData.account_name);
        $('#pensionIdView').text(employeeData.pension_id);
        $('#taxIdView').text(employeeData.tax_id);

        // Populate job details
        $('#employee_idView').text(employeeData.employee_id);
        $('#departmentView').text(employeeData.department);
        $('#job_roleView').text(employeeData.job_role);
        $('#joining_dateView').text(employeeData.joining_date);
        $('#employment_typeView').text(employeeData.employment_type);
        $('#employment_statusView').text(employeeData.employment_status);
        $('#designationView').text(employeeData.designation);
        $('#levelView').text(employeeData.level);
        $('#last_promotion_dateView').text(employeeData.last_promotion_date);
        $('#next_promotion_dateView').text(employeeData.next_promotion_date);
        $('#salaryView').text(employeeData.basic_salary);

        // Populate other information
        $('#emergency_contactsView').text(employeeData.emergency_contacts);
        $('#termination_resignation_dateView').text(employeeData.termination_resignation_date);
        $('#highest_qualificationView').text(employeeData.highest_qualification);
        $('#highest_certificateView').attr('href', employeeData.highest_certificate);
        $('#employment_letterView').attr('href', employeeData.employment_letter);
        $('#skills_qualificationsView').text(employeeData.skills_qualifications);
        $('#next_of_kin_nameView').text(employeeData.next_of_kin_name);
        $('#next_of_kin_relationshipView').text(employeeData.next_of_kin_relationship);
        $('#next_of_kin_phone_numberView').text(employeeData.next_of_kin_phone_number);

        // Populate supervised employees
        let supervisedEmployees = employeeData.supervised_employees;
        let supervisedList = $('#supervised_employeesView');
        supervisedList.empty();
        if (supervisedEmployees.length > 0) {
            $.each(supervisedEmployees, function(index, employee) {
                supervisedList.append(`<li> ${employeeData.first_name}  ${employeeData.last_name}  - ${employeeData.department}</li>`);
            });
        } else {
            supervisedList.append('<li><h5>No supervised employees</h5></li>');
        }

        // Populate timestamps
        $('#created_atView').text(formatDateTime(employeeData.created_at));
        $('#updated_atView').text(formatDateTime(employeeData.updated_at));

        // Show the modal
        $('.spinner-container').hide();
            $('#viewEmpDetailContainer').slideToggle()
            flashMessage(employeeData);
    }

    // Close modal and backdrop
    $('.close').click(function() {
        $('.backdrop').hide();
        $('.empModalContainer').hide();
        if ($('.flash-ajax-message').hasClass('error-message') || $('.flash-ajax-message').hasClass('success-message')) {
            $('.flash-ajax-message').slideToggle();
        }
    });


    // Update employee data

    $('.moreEmpDetail#editEmpDetailBtn').click(function(e) {
        e.preventDefault();
        $('.backdrop').show(),
        $('.spinner-container').show();
        let employeeId = $(this).data('employeeid');
        $.ajax({
            url: `/api/employees/${employeeId}/`,
            method: 'GET',
            dataType: 'json',
            success: function(response) {
                populateEditModal(response);    
            },
            error: function(xhr, status, error) {
                console.error('Error fetching employee data:', error);
                alert('Error fetching employee data');
            }
        });
    })

    function populateEditModal(employeeData) {
        // Personal Information
        $('#eId').val(employeeData.id);
        $('#firstNameEdit').val(employeeData.first_name);
        $('#middleNameEdit').val(employeeData.middle_name);
        $('#lastNameEdit').val(employeeData.last_name);
        $('#phoneNumberEdit').val(employeeData.phone_number);
        $('#emailEdit').val(employeeData.email);
        $('#dobEdit').val(employeeData.dob);
        $('#genderEdit').val(employeeData.gender);
        $('#maritalStatusEdit').val(employeeData.marital_status);
        $('#nationalityEdit').val(employeeData.nationality);
        $('#stateOfOriginEdit').val(employeeData.state_of_origin);
        $('#addressEdit').val(employeeData.address);
        $('#profilePictureEditView').attr('src', employeeData.profile_picture);

        // Bank Information
        $('#bankNameEdit').val(employeeData.bank_name);
        $('#accountNumberEdit').val(employeeData.account_number);
        $('#accountNameEdit').val(employeeData.account_name);
        $('#pensionIdEdit').val(employeeData.pension_id);
        $('#taxIdEdit').val(employeeData.tax_id);

        // Employment Information
        $('#employeeIdEdit').val(employeeData.employee_id);
        $('#departmentEdit').val(employeeData.department);
        $('#jobRoleEdit').val(employeeData.job_role);
        $('#joiningDateEdit').val(formatDateTime(employeeData.joining_date).split(' ')[0]);
        $('#employmentTypeEdit').val(employeeData.employment_type);
        $('#employmentStatusEdit').val(employeeData.employment_status);
        $('#designationEdit').val(employeeData.designation);
        $('#levelEdit').val(employeeData.level);
        $('#lastPromotionDateEdit').val(employeeData.last_promotion_date);
        $('#nextPromotionDateEdit').val(employeeData.next_promotion_date);
        $('#highestQualificationEdit').val(employeeData.highest_qualification);
        $('#salaryEdit').val(employeeData.basic_salary);
        $('#terminationResignationDateEdit').val(employeeData.termination_resignation_date);
        $('#emergencyContactsEdit').val(employeeData.emergency_contacts);
        
        // Supervised Employees
        let supervisedEmployees = employeeData.supervised_employees;
        let supervisedList = $('#supervisedEmployeesEdit');
        supervisedList.empty();
        if (supervisedEmployees.length > 0) {
            supervisedList.append('<option value="" disabled>Select to remove</option>');
            $.each(supervisedEmployees, function(index, employee) {
                let optionText = `${employee.first_name} ${employee.last_name} - ${employee.employee_id}`;
                supervisedList.append(`<option value="${employee.employee_id}">${optionText}</option>`);
            });
        } else {
            supervisedList.append('<option value="" disabled>No supervised employees</option>');
        }
        $('#skillsQualificationsEdit').val(employeeData.skills_qualifications);

        // Next of Kin
        $('#nextOfKinNameEdit').val(employeeData.next_of_kin_name);
        $('#nextOfKinRelationshipEdit').val(employeeData.next_of_kin_relationship);
        $('#nextOfKinPhoneNumberEdit').val(employeeData.next_of_kin_phone_number);
        
        // Show the modal
        $('.spinner-container').hide();
        $('#updateEmpDetailContainer').slideToggle();
    }

    // update employee data with ajax and csfr token
    $('#updateEmployeeBtn').on('click', function(event) {
        event.preventDefault();
        let employeeId = $('#eId').val();
        if (!employeeId || isNaN(employeeId)) {
            alert('Employee ID not found');
            return;
        }
        form = $('#updateEmployeeForm');
        let formData = new FormData($('#updateEmployeeForm')[0]);
    
        // Get the CSRF token from hidden input field
        let csrfToken = $('[name=csrfmiddlewaretoken]').val();
    
        $.ajax({
            url: `/updateEmployee/${employeeId}/`,
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
    
            // Include CSRF token in the headers
            headers: {
                'X-CSRFToken': csrfToken
            },
    
            success: function(response) {
                flashMessage(response);
                $('#updateEmpDetailContainer').slideToggle();
                $('.backdrop').hide();
                form.trigger('reset');
            },
            error: function(xhr, status, error) {
                console.error('Error updating employee data:', error);
                flashMessage(error);
                // $('.flash-ajax-message').slideToggle(
                //     timeoutFlashMessage()
                // );
            }
        });

    });
    $('#updateEmployeeBtn').click(function() {
        $('.flash-ajax-message').slideToggle(
            timeoutFlashMessage()
        );
});

    // hide empModalContainer when cancelBtn is clicked
    $('.cancelBtn').click(function() {
        $('.backdrop').hide();
        $('.empModalContainer').hide();
        $('#updateBankContainer').hide();
    });

    // Archive employee
    $('.moreEmpDetail#archiveEmpDetailBtn').click(function(e) {
        e.preventDefault();
        $('.spinner-container').show();
        let employeeId = $(this).data('employeeid');
        // let rowToRemove = $(this).closest('tr'); // Get the row to remove

        $('#archive-modal').slideToggle(function(){
            $('.spinner-container').hide();
        });
        $('#submitArchiveBtn').click(function(e) {
            e.preventDefault();
            $('.spinner-container').show();
            form = $('#archiveEmployeeForm');
            let formData = new FormData($('#archiveEmployeeForm')[0]);
            // Get the CSRF token from hidden input field
            let csrfToken = $('#archiveEmployeeForm input[name=csrfmiddlewaretoken]').val();
            $.ajax({
                url: `/archiveEmployee/${employeeId}/`,
                method: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                // Include CSRF token in the headers
                headers: {
                    'X-CSRFToken': csrfToken
                },
                success: function(response) {
                    $('.spinner-container').hide();
                    window.location.reload()
                    // flashMessage(response);
                    // $('#archive-modal').slideToggle();
                    // $('.backdrop').hide();
                    // form.trigger('reset');
                    // flashMessage(response);

                    // // Remove the row from the table
                    // rowToRemove.remove();
                },
                error: function(xhr, status, error) {
                    console.error('Error archiving employee:', error);
                    flashMessage(error);
                }
            });
        });
    });

    // unarchive employee
    $('.EmpArchiveBtn').click(function(e) {
        e.preventDefault();
        $('.spinner-container').show();
        let employeeId = $(this).data('employeeid');
        $('#unarchive-modal').slideToggle(function(){
            $('.spinner-container').hide();
        });
        $('#submitRestoreBtn').click(function(e) {
            e.preventDefault();
            $('.spinner-container').show();
            $.ajax({
                url: `/restoreArchive/${employeeId}/`,
                method: 'GET',
                processData: false,
                contentType: false,
                success: function() {
                    $('.spinner-container').hide();
                    window.location.reload()
                },
                error: function(xhr, status, error) {
                    console.error('Error restoring employee:', error);
                    flashMessage(error);
                }
            });
        });
    });

    // delete employee
    $('.moreEmpDetail.DelArchiveBtn, .moreEmpDetail#deleteEmpDetailBtn').click(function(e) {
        e.preventDefault();
        // $('.spinner-container').show();
        let employeeId = $(this).data('employeeid');
        $('#delete-modal').slideToggle();
        $('#submitDeleteBtn').off().click(function(e) {
            e.preventDefault();
            $('.spinner-container').show();
            $.ajax({
                url: `/deleteEmployee/${employeeId}/`,
                method: 'GET',
                processData: false,
                contentType: false,
                success: function() {
                    $('.spinner-container').hide();
                    window.location.reload()
                },
                error: function(xhr, status, error) {
                    console.error('Error deleting employee:', error);
                    flashMessage(error);
                }
            });
        });
        $('.archive-submit-btn').off().click(function(e) {
            e.preventDefault();
            $('#delete-modal').slideUp();
            $('#archive-modal2').slideDown();
        });
        $('#submitArchiveBtn2').off().click(function(e) {
            e.preventDefault();
            // Ajax call to archive employee
            form = $('#archiveEmployeeForm2');
            let formData = new FormData($('#archiveEmployeeForm2')[0]);
            // Get the CSRF token from hidden input field
            let csrfToken = $('#archiveEmployeeForm2 input[name=csrfmiddlewaretoken]').val();
            $.ajax({
                url: `/archiveEmployee/${employeeId}/`,
                method: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                // Include CSRF token in the headers
                headers: {
                    'X-CSRFToken': csrfToken
                },
                success: function(response) {
                    $('.spinner-container').hide();
                    window.location.reload()
                },
                error: function(xhr, status, error) {
                    console.error('Error archiving employee:', error);
                    flashMessage(error);
                }
            });
        });

        });
    
    // accept and decline leave
    $('.approve-btn').click(function() {
        let leaveId = $(this).data('leaveid');
        $.post(`/manageLeaveRequest/${leaveId}/`, { action: 'accept' }, function(data) {
            if (data.error) {
                flashMessage(data.error);
            }
            window.location.reload()
        });
    });

    $('.decline-btn').click(function() {
        let leaveId = $(this).data('leaveid');
        $.post(`/manageLeaveRequest/${leaveId}/`, { action: 'decline' }, function(data) {
            // Handle success or error response from the server
            if (data.error) {
                flashMessage(data.error);
            }
            window.location.reload()
            message = "Success"
            flashMessage(message);

         });
    });


    // update bank 

    // open updateBankContainer modal when edit-bank is clicked
    $('.edit-bank').click(function(e) {
        e.preventDefault();
        $('.spinner-container').show();
        let employeeId = $(this).data('employeeid');
        $.ajax({
            url: `/api/employees/${employeeId}/`,
            method: 'GET',
            dataType: 'json',
            success: function(response) {
                // populate bank details
                $('#empId').val(response.id)
                $('#bankNameBank').val(response.bank_name);
                $('#accountNumberBank').val(response.account_number);
                $('#accountNameBank').val(response.account_name);
                $('#pensionIdBank').val(response.pension_id);
                $('#taxIdBank').val(response.tax_id);
                
                $('.spinner-container').hide();
                $('#updateBankContainer').slideToggle();
            },
            error: function(xhr, status, error) {
                flashMessage(error);
                $('.flash-ajax-message').slideToggle(
                    timeoutFlashMessage()
                );
                console.error('Error fetching employee data:', error);
            }
        });
    });

    $('#updateEmployeeBankBtn').on('click', function(event) {
        event.preventDefault();
        let employeeId = $('#empId').val();
        if (!employeeId || isNaN(employeeId)) {
            alert('Employee ID not found');
            return;
        }
        form = $('#updateBankForm');
        let formData = new FormData($('#updateBankForm')[0]);
    
        // Get the CSRF token from hidden input field
        let csrfToken = $('#updateBankForm input[name=csrfmiddlewaretoken]').val();
    
        $.ajax({
            url: `/updateEmployee/${employeeId}/`,
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
    
            // Include CSRF token in the headers
            headers: {
                'X-CSRFToken': csrfToken
            },
    
            success: function(response) {
                form.trigger('reset');
                window.location.reload()
            },
            error: function(xhr, status, error) {
                console.error('Error updating employee data:', error);
                flashMessage(error);
                // $('.flash-ajax-message').slideToggle(
                //     timeoutFlashMessage()
                // );
            }
        });

    });


});