$(document).ready(function () {
    // TODO: Bring this entire script to less that 500 lines. Use functions to reduce the number of lines
    // TODO: consider the impact of using document.on vs document.one (it seems using on is expensive)
    $('#add-employee').submit(function(){
        $('.spinner-container').show()
    })

    // Load content dynamically on link click
    $('.featuresItem').click(function () {
        content = $(this).data('content');
        $('.mgt').hide();
        $('.featuresItem').removeClass('active')
        $(this).addClass('active')
        $(`.${content}`).show();
    });
    $('.featuresToggleContainer').click(function () {
        if ($(window).outerWidth() <= 768) {
            $(this).toggleClass('active');
            $('.featuresList').slideToggle();
        }
    });

    // Function to close Feature list when window is resized to larger than 900px
    $(window).resize(function () {
        if ($(window).outerWidth() > 768) {
            $('.featuresList').slideDown();
            $('.actions').slideDown();
        } 

        /**
         * Uncomment the else block to hide the features list when the window is resized to less than 768px
         * this was commented because of the behavior on mobile devices scroll
        
        else {
            $('.featuresList').slideUp();
            $('.actions').slideUp();
        } 
        */
    });

    // // Handle mouse enter and leave events for the left pane
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

        // Account Management tab
        $(".tab5").on("click", function() {
            $(".tab5").removeClass("active");
            $(this).addClass("active");
            let tab = $(this).data("tab5");
            $(".tab-contents5").hide();
            $(`#${tab}`).show();
        });

        // Transfer Management tab
        $(".tab6").on("click", function() {
            $(".tab6").removeClass("active");
            $(this).addClass("active");
            let tab = $(this).data("tab6");
            $(".tab-contents6").hide();
            $(`#${tab}`).show();
        });
        

        
        // Menu Toggle
        $(".menuToggle").on("click", function() {
            if ($(window).outerWidth() < 850) {
                $(".actions").slideToggle();
            }
        });


        // Close the dropdown menu when the user clicks outside of it
        $(document).on('click', '.dropdown', function(event) { // without attaching the dropdown to the document, it won't work then dataTable dynamically loads the DOM
            event.stopPropagation(); // When DOM Is loaded, only elements on the page are clickable, when dataTable loads next page, the dropdown events are not attached to the new elements, so we attach the event to the document
            let dropdownMenu = $(this).find('.dropdown-menu');
            if (dropdownMenu.hasClass('open')) {
                dropdownMenu.slideUp().removeClass('open');
            } else {
                $('.dropdown-menu.open').hide().removeClass('open');
                dropdownMenu.slideDown().addClass('open');
            }
        });

        
        // Close dropdown menu when clicking outside
        $(document).on('click', function() {
            $('.dropdown-menu.open').slideUp().removeClass('open');
        });

        $(document).on('click', '.moreEmpDetail.viewEmpDetailBtn', function(e) { 
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
                    openModal('errorModal');
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
        if (employeeData.middle_name) {
            $('#empFullNameView').text(`${employeeData.first_name} ${employeeData.middle_name[0].toUpperCase()}. ${employeeData.last_name}`);
        }
        else {
            $('#empFullNameView').text(`${employeeData.first_name} ${employeeData.last_name}`);
        }
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
            // openModal('successModal');
    }

    // Close modal and backdrop
    $(document).on('click', '.modal-content .close, span.close, .main_block .close, .multiUpload .close', function() {
        $('.backdrop').hide();
        $('.empModalContainer').hide();
    });
    


    // Update employee data
    $(document).on('click', '.moreEmpDetail.editEmpDetailBtn', function(e) {
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
        $('#eId').val(employeeData.employee_id);
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
        $('#updateEmpDetailContainer').slideDown();
    }

    // update employee data with ajax and csfr token
    $(document).on('click', '#updateEmployeeBtn', function(e) {
        e.preventDefault();
        $('.spinner-container').show();

        let employeeId = $('#eId').val();
        if (!employeeId) {
            $('.spinner-container').hide();
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
                openModal('successModal');
                $('.spinner-container').hide();
                $('#updateEmpDetailContainer').slideToggle();
                $('.backdrop').hide();
                form.trigger('reset');
            },
            error: function(xhr, status, error) {
                console.error('Error updating employee data:', error);
                openModal('errorModal');
                $('.spinner-container').hide();
            }
        });

    });

    // hide empModalContainer when cancelBtn is clicked
    $(document).on('click', '.cancelBtn', function() {
        $('.backdrop').hide();
        $('.empModalContainer').hide();
        $('#updateBankContainer').hide();
    });

    // Archive employee
    $(document).on('click', '.moreEmpDetail.archiveEmpDetailBtn', function(e) {
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
                },
                error: function(xhr, status, error) {
                    console.error('Error archiving employee:', error);
                    openModal('errorModal');
                }
            });
        });
    });

    // unarchive employee
    $(document).on('click', '.EmpArchiveBtn', function(e) {
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
                    openModal('errorModal');
                }
            });
        });
    });

    // delete employee
    $(document).on('click', '.moreEmpDetail.DelArchiveBtn, .moreEmpDetail.deleteEmpDetailBtn', function(e) {
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
                    openModal('errorModal');
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
            $('.spinner-container').show();
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
                    openModal('errorModal');
                }
            });
        });

        });
    
    
        $(document).on('change', '#endDate', function() {
        let startDate = new Date($('#startDate').val());
        let endDate = new Date($(this).val());

        if (endDate < startDate) {
            openModal('errorModal', 'End date cannot be earlier than start date');
            $(this).val($('#startDate').val());// Reset the end date input value to the start date value
        }
    });

    $(document).on('click', '.approve-btn', function() {
        let leaveId = $(this).data('leaveid');
        $.post(`/manageLeaveRequest/${leaveId}/`, { action: 'accept' }, function(data) {
            if (data.error) {
                openModal('errorModal');
                console.error('Error accepting leave request:', data.error);
                }
            window.location.reload()
        });
    });

    $(document).on('click', '.decline-btn', function() {
        let leaveId = $(this).data('leaveid');
        $.post(`/manageLeaveRequest/${leaveId}/`, { action: 'decline' }, function(data) {
            // Handle success or error response from the server
            if (data.error) {
                openModal('errorModal');
                console.error('Error declining leave request:', data.error);
            }
            window.location.reload()
         });
    });
    // $('.dataTable').click(()=> alert('dtable clicked'))

    // update bank 

    // open updateBankContainer modal when edit-bank is clicked
    $(document).on('click', '.edit-bank', function(e) {
        e.preventDefault();
        $('.spinner-container').show();
        let employeeId = $(this).data('employeeid');
        $.ajax({
            url: `/api/employees/${employeeId}/`,
            method: 'GET',
            dataType: 'json',
            success: function(response) {
                // populate bank details
                $('#empId').val(response.employee_id)
                $('#bankNameBank').val(response.bank_name);
                $('#accountNumberBank').val(response.account_number);
                $('#accountNameBank').val(response.account_name);
                $('#pensionIdBank').val(response.pension_id);
                $('#taxIdBank').val(response.tax_id);
                
                $('.spinner-container').hide();
                $('#updateBankContainer').slideToggle();
            },
            error: function(xhr, status, error) {
                openModal('errorModal');
                console.error('Error fetching employee data:', error);
            }
        });
    });

    $(document).on('click', '#updateEmployeeBankBtn', function(e) {
        e.preventDefault();
        $('.spinner-container').show();
        let employeeId = $('#empId').val();
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
                openModal('errorModal');
            }
        });

    });


    // SEARCH FUNCTIONALITY
    // $('.search-bar input').on('keyup', function() {
    //     let searchQuery = $(this).val().trim().toLowerCase();
    //     $('.s-card').each(function() {
    //         let field1 = $(this).find('.sf1').text().toLowerCase();
    //         let field2 = $(this).find('.sf2').text().toLowerCase();
    //         let field3 = $(this).find('.sf3').text().toLowerCase();
    //         let field4 = $(this).find('.sf4').text().toLowerCase();
    //         let field5 = $(this).find('.sf5').text().toLowerCase();
    //         if (field1.includes(searchQuery) || field2.includes(searchQuery)
    //          || field3.includes(searchQuery) || field4.includes(searchQuery) || field5.includes(searchQuery)) {
    //         $(this).show();
    //         } else {
    //             $(this).hide();
    //         }
    //     });
    // });

    $('input[type="search"]').attr('placeholder', 'Enter search text');


    // populate leave employee id
    $('#employeeName').change(function() {
        let selectedEmployeeId = $(this).val();
        $('#employeeID').val(selectedEmployeeId);
    });



    // Attach click event handler to the link
    $('#add-employee .nav-link').click(function() {
        // Check if the clicked link has the specific href attribute
        if ($(this).attr('href') === '#employment-details') {
            // Generate random string
            let randomString = generateRandomString();
            if (!$('#id_employee_id').val()) {
                $('#id_employee_id').val(randomString);
            }
        }
    });
    
    // Function to generate random string as auto employee_id
    function generateRandomString() {
        let chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        let digits = '0123456789';
        let randomString = '';
        for (let i = 0; i < 2; i++) {
            randomString += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        for (let i = 0; i < 4; i++) {
            randomString += digits.charAt(Math.floor(Math.random() * digits.length));
        }
        return randomString;
    }
    
    function validateDate(dateString) {
        // Parse the entered date string
        let date = new Date(dateString);
        // Check if the date is valid
        if (isNaN(date.getTime())) {
            return false; // Invalid date
        }
        // Calculate the age from the entered date
        let today = new Date();
        let age = today.getFullYear() - date.getFullYear();
        let monthDiff = today.getMonth() - date.getMonth();
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < date.getDate())) {
            age--; // Adjust age if birthday hasn't occurred yet
        }
        // Check if the age is within the specified range (12 to 150 years)
        return age >= 12 && age <= 150;
    }

    // Event listener for blur event on #id_dob and #dob elements
    $('#id_dob, #dob').on('input', function() {
        let dob = $(this).val(); // Get the entered date of birth
        // Validate the date of birth
        if (!validateDate(dob)) {
            $(this).css({
                'background': 'rgba(182, 9, 9, 0.802)',
                'color': 'white',
            })
        }
        else {
                $(this).css({
                    'background': '#fff',
                    'color': '#495057',
                })
        }
    });


    /**
     * 
     * This section handles the profile picture upload functionality
     */
    // Open the modal
    function openModal(modalId, message=null) {
        if (message && modalId === 'errorModal') {
            $(`#${modalId} p`).text(message);
        }
        $(`#${modalId}`).css("display", "block");
        let errMsg = 'There was an error processing your request. Please try again later'
        if ($('#errorVal').text() !== errMsg){
            $(document).one('click',()=>{$(`#errorVal`).text(errMsg)})
        }
    }
    
    // Close the modal
    function closeModal() {
        $('.backdrop').hide();
        $(".modale").css("display", "none");
    }

    $('.profile_dp, .plus_container i').click(function() {
        // Simulate a click on the file input when the plus sign or photo is clicked
        $(this).closest('.profile-picture').find('.profile-picture-input').click();
    });
    
    $('.profile-picture-input').change(function() {
        $('.spinner-container').show();
        // Get the selected file
        openModal('uploadPhotoModal');
        $('.spinner-container').hide()
        let file = $(this)[0].files[0];
        let isEmp = $(this).data('empdata');
        let url;
    
        // Handle the click event of the proceedUploadBtn only once
        $('.proceedUploadBtn').one('click', function() {
            if (isEmp) {
                let emp_id = $('#eId').val();
                url = `/user/update_dp/${emp_id}/`;
            } else {
                url = `/user/update_dp/`;
            }
    
            let formData = new FormData();
            formData.append('profile_picture', file);
    
            // Send AJAX request to update profile picture
            $('.spinner-container').show();
            $.ajax({
                url: url,
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(data) {
                    $('.tiny_images, .profile_dp').attr('src', data.profile_picture);
                    $('.spinner-container').hide();
                    openModal('successModal');
                },
                error: function(e) {
                    $('.spinner-container').hide();
                    openModal('errorModal');
                    console.error(e)
                }
            });

            $('.cancelConfirmBtn').click(function(){
                closeModal()
                $('.profile-picture-input').val('')
            })
        });
    });

    $('.closeModal').click(function() {
        $('.modale').hide();
        $('.profile-picture-input').val('');
    });

    //   close modals when document is clicked
    $(document).click(function(){
        $('.clickClose').hide();
        $('.profile-picture-input').val('');
    })

    // Upload employee data from excel or csv file
    $('#uploadDataBtn').click(function() {
        $('.backdrop').show();
        $('#empUploadForm').show();
    });

    $('#uploadPRollBtn').click(function() {
        $('.backdrop').show();
        $('#payrollUploadForm').show();
    });


    // Resolve last row issue in dataTable
    $('.dataTable').on('click', '.dropdown', function() {
        let dropdownMenu = $(this).find('.dropdown-menu');
        let tableTop = $(this).closest('.dataTable').offset().top;
        let tableHeight = $(this).closest('.dataTable').outerHeight();
        let dropdownBottom = $(this).offset().top + dropdownMenu.outerHeight();
        
        if (dropdownBottom > (tableTop + tableHeight)) {
            dropdownMenu.css('top', 'auto');
            dropdownMenu.css('bottom', '100%');
        } else {
            dropdownMenu.css('top', '100%');
            dropdownMenu.css('bottom', 'auto');
        }
        
        dropdownMenu.toggle();
        });

        });

$(document).ready(function() {
    let features = $('.feature'); // Select all features
    let index = 0; // Initialize index for tracking active feature

    function slideFeatures() {
        // Hide current feature
        features.eq(index).removeClass('active');
        // Increment index and loop back to the start if necessary
        index = (index + 1) % features.length;
        // Show next feature
        features.eq(index).addClass('active');
    }

    // Display the first feature initially
    features.eq(index).addClass('active');

    // Slide features every 3 seconds
    setInterval(slideFeatures, 3000);
});
