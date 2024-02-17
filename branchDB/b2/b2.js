$(document).ready(function () {
    // Load default content
    $('#content').load('leave_management.html');

    // Load content dynamically on link click
    $('#employeeManagement').click(function (e) {
        e.preventDefault();
        $('#content').load('employee_management.html');
    });

    $('#leaveManagement').click(function (e) {
        e.preventDefault();
        $('#content').load('leave_management.html');
    });

    $('#payrollManagement').click(function (e) {
        e.preventDefault();
        $('#content').load('payroll_management.html');
    });

    $('#performanceReporting').click(function (e) {
        e.preventDefault();
        $('#content').load('performance_reporting.html');
    });

    $('#accountSettings').click(function (e) {
        e.preventDefault();
        $('#content').load('account_settings.html');
    });

    // Show default tab content (Leave Requests)
    $('#leave-requests').show();

        // Function to toggle Feature list on heading click for screens less than 900px
        $('.featuresToggle').click(function () {
            if ($(window).width() <= 768) {
                $('.featuresList').slideToggle();
            }
        });
        $('.featuresItem').click(function () {
            if ($(window).width() <= 768) {
                $('.featuresList').slideToggle();
            }
        });

        // Function to close Feature list when window is resized to larger than 900px
        $(window).resize(function () {
            if ($(window).width() > 768) {
                $('.featuresList').slideDown();
            }
        });

        // display leave requests when #payrollManagement is clicked
    });

