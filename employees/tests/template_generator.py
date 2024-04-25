import pandas as pd

# Define the headers corresponding to the fields in the Employee model
employee_headers = [
    'First Name', 'Last Name', 'Middle name', 'Date of birth', 'Gender',
    'Marital status', 'email address', 'Address', 'Nationality', 'State of origin',
    'Phone number', 'Employee ID', 'Department/division', 'Job role', 'Date employed',
    'Employment type', 'Employment status', 'Designation', 'Level', 'Last promotion date',
    'Next promotion date', 'Salary', 'bank name', 'account number', 'account name',
    'pension ID', 'tax ID', 'Emergency contacts', 'Date of termination/resignation',
    'Highest qualification', 'Skills/qualifications', 'Next of kin name', 'Next of kin relationship',
    'Next of kin phone number'
]

# Sample data for two records
employee_data = [
    {'First Name': 'John', 'Last Name': 'Doe', 'Middle name': 'Michael', 'Date of birth': '1990-01-01', 'Gender': 'Male',
     'Marital status': 'Single', 'email address': 'john.doe@example.com', 'Address': '123 Main St', 'Nationality': 'American',
     'State of origin': 'New York', 'Phone number': '123-456-7890', 'Employee ID': 'EMP001', 'Department/division': 'IT',
     'Job role': 'Software Engineer', 'Date employed': '2022-01-01', 'Employment type': 'Full-time', 'Employment status': 'Active',
     'Designation': 'Employee', 'Level': 'Mid-level', 'Last promotion date': '2023-01-01', 'Next promotion date': '2024-01-01',
     'Salary': 50000, 'bank name': 'ABC Bank', 'account number': '1234567890', 'account name': 'John Doe', 'pension ID': 'PENSION001',
     'tax ID': 'TAX001', 'Emergency contacts': 'Jane Doe (Spouse): 987-654-3210', 'Date of termination/resignation': '',
     'Highest qualification': 'Bachelor\'s Degree', 'Skills/qualifications': 'Python, Java, SQL', 'Next of kin name': 'Jane Doe', 'Next of kin relationship': 'Spouse',
     'Next of kin phone number': '987-654-3210'},
    {'First Name': 'Emma', 'Last Name': 'Smith', 'Middle name': '', 'Date of birth': '', 'Gender': '',
     'Marital status': '', 'email address': 'emmasmith@example.com', 'Address': '', 'Nationality': '', 'State of origin': '',
     'Phone number': '', 'Employee ID': '', 'Department/division': '', 'Job role': '', 'Date employed': '',
     'Employment type': 'Part-time', 'Employment status': 'Active', 'Designation': 'Supervisor', 'Level': '', 'Last promotion date': '',
     'Next promotion date': '', 'Salary': '', 'bank name': '', 'account number': '', 'account name': '',
     'pension ID': '', 'tax ID': '', 'Emergency contacts': 'Emma Smith (Lawyer)', 'Date of termination/resignation': '',
     'Highest qualification': '', 'Skills/qualifications': '', 'Next of kin name': '', 'Next of kin relationship': '',
     'Next of kin phone number': ''}
]

def generate_template(headers, data, file_format1='csv', file_format2='xlsx', file_name=None):
    # Merge headers with data
    df = pd.DataFrame(data, columns=headers)

    # Add serial number (SN) column
    df.insert(0, 'SN', range(1, len(df) + 1))

    # Save DataFrame to filename.file_format1 or default to CSV

    csv_template_file = f"employees/tests/files/csv/{file_name}.{file_format1}"
    df.to_csv(csv_template_file, index=False)
    print(f'CSV template with sample data saved as: {csv_template_file}')

    # Save DataFrame to Excel file
    excel_template_file = f"employees/tests/files/excel/{file_name}.{file_format2}"
    df.to_excel(excel_template_file, index=False)
    print(f'Excel template with sample data saved as: {excel_template_file}')

# Generate template for Employee model
# generate_template(employee_headers, employee_data, 'csv', 'employee_template')
# generate_template(employee_headers, employee_data, 'xlsx', 'employee_template')


# Define the headers corresponding to the fields in the payroll model
payroll_headers = [
    'Employee ID','Year', 'Month', 'Payment Status', 'Housing Allowance', 'Transport Allowance',
    'Feeding Allowance', 'Utility Allowance', 'Other Allowance', 'Tax', 'Pension',
    'Loan', 'Other Deductions', 'Late Penalty', 'Absent Penalty', 'Overtime Bonus',
    'Performance Bonus', 'Performance Penalty', 'Basic Salary'
]

# Sample data for two records
payroll_data = [
    {'Year': 2024, 'Month': 1, 'Payment Status': 'Pending', 'Housing Allowance': 5000, 'Transport Allowance': 3000,
     'Feeding Allowance': 2000, 'Utility Allowance': 1000, 'Other Allowance': 0, 'Tax': 10000, 'Pension': 5000,
     'Loan': 0, 'Other Deductions': 0, 'Late Penalty': 0, 'Absent Penalty': 0, 'Overtime Bonus': 0,
     'Performance Bonus': 0, 'Performance Penalty': 0, 'Basic Salary': 50000, 'Employee ID': '4298RC'},
    {'Year': 2024, 'Month': 2, 'Payment Status': 'Paid', 'Housing Allowance': 5000, 'Transport Allowance': 3000,
     'Feeding Allowance': 2000, 'Utility Allowance': 1000, 'Other Allowance': 0, 'Tax': 10000, 'Pension': 5000,
     'Loan': 0, 'Other Deductions': 0, 'Late Penalty': 0, 'Absent Penalty': 0, 'Overtime Bonus': 0,
     'Performance Bonus': 0, 'Performance Penalty': 0, 'Basic Salary': 50000, 'Employee ID': '3112LJ'}
]

# Generate template for Payroll model
generate_template(headers=payroll_headers, data=payroll_data, file_name='payroll_template')
generate_template(headers=payroll_headers, data=payroll_data, file_name='payroll_template')
