// scripts.js

$(document).ready(function() {
    // Function to open the employee management section and close other sections
    function openEmployeesSection() {
        $(".tabcontent").hide(); // Hide all sections
        $("#employees").toggle(); // Show the employees section
        $(".sidebar a").removeClass("active"); // Remove active class from all sidebar links
        $(".employeesLink").addClass("active"); // Add active class to employees link
    }

    // Show employee management section when clicked on the corresponding link
    $(".employeesLink").click(function() {
        openEmployeesSection();
    });

    // Open modal for adding employee
    $("#addEmployeeBtn").click(function() {
        $("#employeeModal").css("display", "block");
    });

    // Close modal for adding/updating employee
    $(".modal .close").click(function() {
        $(".modal").css("display", "none");
    });

    // Handle form submission for adding/updating employee
    $("#employeeForm").submit(function(event) {
        event.preventDefault();
        // Add code to handle form submission (e.g., AJAX request)
        // After successful submission, close modal and update employee list
        $(".modal").css("display", "none");
        // You can reload the employee list or perform other actions here
    });

    // AJAX request to fetch and display employee list
    function displayEmployeeList() {
        // Dummy data for demonstration
        const employees = [
            { id: 1, firstName: "John", lastName: "Doe", email: "john@example.com" },
            { id: 2, firstName: "Jane", lastName: "Smith", email: "jane@example.com" },
            // Additional dummy data can be added
        ];

        const employeeListContainer = $("#employeeList");
        employeeListContainer.empty(); // Clear previous list

        employees.forEach(employee => {
            // Create employee card HTML dynamically
            const employeeCard = `
                <div class="employee-card">
                    <h3>${employee.firstName} ${employee.lastName}</h3>
                    <p>Email: ${employee.email}</p>
                    <!-- Additional employee details can be added here -->
                </div>
            `;
            employeeListContainer.append(employeeCard); // Append card to container
        });
    }

    // Display employee list when employee management section is opened
    openEmployeesSection();
    displayEmployeeList();








    // Open modal for adding employee
    $("#addEmployee").click(function() {
        $("#addEmployeeModal").css("display", "block");
    });

    // Close modal for adding employee
    $("#addEmployeeModal .close").click(function() {
        $("#addEmployeeModal").css("display", "none");
    });

    // Open modal for updating employee
    $("#updateEmployee").click(function() {
        $("#updateEmployeeModal").css("display", "block");
    });

    // Close modal for updating employee
    $("#updateEmployeeModal .close").click(function() {
        $("#updateEmployeeModal").css("display", "none");
    });

    // Open modal for deleting employee
    $("#deleteEmployee").click(function() {
        $("#deleteEmployeeModal").css("display", "block");
    });

    // Close modal for deleting employee
    $("#deleteEmployeeModal .close").click(function() {
        $("#deleteEmployeeModal").css("display", "none");
    });

    // Open modal for archiving employee
    $("#archiveEmployee").click(function() {
        $("#archiveEmployeeModal").css("display", "block");
    });

    // Close modal for archiving employee
    $("#archiveEmployeeModal .close").click(function() {
        $("#archiveEmployeeModal").css("display", "none");
    });

    // AJAX requests and functionality for other features can be added here
});

