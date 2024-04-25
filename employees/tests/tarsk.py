from celery import shared_task
from django.shortcuts import get_object_or_404
from employees.models import Branch, AdminUser, Employee
from employees.celery.tasks import generate_employee_id

# Create a list to hold employee data and simulate possible errors
@shared_task
def test_errors(branch_id=None, user_id=None, *args, **kwargs):
    branch = get_object_or_404(Branch, branch_id=branch_id)
    admin = get_object_or_404(AdminUser, pk=user_id)
    employee_data = [
        {
            'First Name': 'Festa',
            'Last Name': 'Owelle',
            'Middle name': 'F.',
            'Date of birth': '1990-01-01',
            'Gender': 'Male',
            'Marital status': 'Single',
            'email address': 'space@example.com',
            'Address': '123 Main St',
            'Nationality': 'American',
            'State of origin': 'New York',
            'Phone number': '123-456-7890',
            'Department/division': 'IT',
            'Job role': 'Software Engineer',
            'Joining date': '2022-01-01',
            'Employment type': 'Tired',
            'Employment status': 'Action',
            'Designation': 'Employee',
            'Level': 'Mid-level',
            'Salary': 50000,
            'bank name': 'UBA Bank',
            'account number': 1234567890,
            'account name': 'Jimmy Franklin',
            'pension ID': 'PENSION001',
            'tax ID': 'TAX001',
            'Emergency contacts': 'Jimmy Franklin, 123-456-7890',
            'Highest qualification': "Bachelor's Degree",
            'Skills/qualifications': 'Python, Java, SQL',
            'Archived status': False,
            # Missing Employee ID intentionally
        }
        for _ in range(10)
    ]

    # Set 3 employee IDs to None to simulate missing data
    employee_data[7]['Employee ID'] = None
    employee_data[8]['Employee ID'] = None
    employee_data[9]['Employee ID'] = None

    # Process employee data
    for count, data in enumerate(employee_data):
        data['email address'] = data[f"email address"] + str(count)
        try:
            # Create employee with the provided data
            employee = Employee.objects.create(
                first_name=data.get('First Name'),
                last_name=data.get('Last Name'),
                middle_name=data.get('Middle name'),
                dob=data.get('Date of birth'),
                gender=data.get('Gender'),
                marital_status=data.get('Marital status'),
                email=data.get('email address'),
                address=data.get('Address'),
                nationality=data.get('Nationality'),
                state_of_origin=data.get('State of origin'),
                phone_number=data.get('Phone number'),
                employee_id=data.get('Employee ID')  or generate_employee_id(),
                department=data.get('Department/division'),
                job_role=data.get('Job role'),
                joining_date=data.get('Joining date'),
                employment_type=data.get('Employment type'),
                employment_status=data.get('Employment status'),
                designation=data.get('Designation'),
                level=data.get('Level'),
                basic_salary=data.get('Salary'),
                bank_name=data.get('bank name'),
                account_number=data.get('account number'),
                account_name=data.get('account name'),
                pension_id=data.get('pension ID'),
                tax_id=data.get('tax ID'),
                emergency_contacts=data.get('Emergency contacts'),
                highest_qualification=data.get('Highest qualification'),
                skills_qualifications=data.get('Skills/qualifications'),
                is_archived=data.get('Archived status'),
                branch=branch,
                adminuser=admin
                # No need to specify other fields as they have default values
            )
            print(f"Employee {employee.first_name} {employee.last_name} created successfully.")
        except Exception as e:
            print(f"Error creating employee: {e}")

