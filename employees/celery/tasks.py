""" Tasks for asynchronous processing - celery"""

from celery import shared_task
from django.shortcuts import get_object_or_404
import pandas as pd
from io import BytesIO
from ..models import Employee, Branch, AdminUser, Payroll
import datetime
import random, string
from django.core.mail import send_mail
from smtplib import SMTPException
from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string


# create send signup email
@shared_task
def send_welcome_mail(recipient, email, pwd, username):
    subject = "Welcome to WorkForceHub!"
    message = f"""
        <html>
        <head></head>
        <body>
            <p>Dear {username},</p>

            <p>Welcome to WorkForceHub! We are excited to have you on board.</p>

            <p>Your account has been successfully created. Below are your login details:</p>

            <ul>
                <li>Username: {username}</li>
                <li>Email: {email}</li>
                <li>Password: {pwd}</li>
            </ul>

            <p>To get started, please log in using the credentials provided above.</p>

            <p>If you have any questions, please don't hesitate to reach out to our friendly support team <a href="mailto:onlinekingsley@gmail.com">here</a> or send a reply to this mail.</p>

            <p>Thank you and welcome aboard!</p>

            <p>Best regards,<br/>
            <a href="mailto:onlinekingsley@gmail.com">Kingsley C. Chime</a><br/>
            WorkForceHub Team</p>
        </body>
        </html>
        """
    email = EmailMultiAlternatives(
        subject,
        from_email=None,
        to=[recipient],
    )
    email.attach_alternative(message, "text/html")
    try:
        email.send()
        return True
    except SMTPException as e:
        error_message = f'Failed to send welcome email to {recipient}: {e}'
        return error_message

# create send password reset email
@shared_task
def send_password_reset_email(recipient, token):
    subject = "Password Reset Code"
    message = f"Your password reset code is {token} (expires in one hour).\n\nPlease do not share this code with anyone\nIf you didn't request this pin, we recommend you change your WorkForceHub password.\n\nRegards, \nKingsley, WorkForceHub Team"
    try:
        send_mail(subject=subject, from_email=None, message=message, recipient_list=[recipient])
        return True
    except SMTPException as e:
        error_message = f'Failed to send welcome email to {recipient}: {e}'
        return error_message

    
def generate_employee_id():
    """Generate 4 digits and 2 Uppercase employee ID"""
    while True:
        nums = ''.join(random.choices(string.digits, k=4))
        chars = ''.join(random.choices(string.ascii_uppercase, k=2))
        employee_id = nums + chars
        # Check if the first character is not zero
        if employee_id[0] != '0' and not Employee.objects.filter(employee_id=employee_id).exists():
            return employee_id
 
# process employee creation
@shared_task
def process_employee_data(file_content:bytes=None, filename:str=None, branch_id:str = None, user_id:int=None, *args, **kwargs):
    try:
        # Determine file format based on filename extension
        if filename.lower().endswith('.xls') or filename.lower().endswith('.xlsx'):
            df = pd.read_excel(BytesIO(file_content))
        elif filename.lower().endswith('.csv'):
            df = pd.read_csv(BytesIO(file_content))
        else:
            # Handle unsupported file formats
            return {'success': False, 'message': 'Unsupported file format.'}
        
        error_messages = [] # List to store error messages
        employee_ids = [] # List to store employee IDs
        
            # Iterate over the rows in the DataFrame and create employees
        for _, row in df.iterrows():
            try:
                branch = Branch.objects.get(branch_id=branch_id)
                admin = get_object_or_404(AdminUser, pk=user_id)
                employee = Employee.objects.create(
                    first_name=row.get('First Name', 'None'),
                    last_name=row.get('Last Name', 'None'),
                    middle_name=row.get('Middle name'),
                    dob = datetime.datetime.strptime(str(row.get('Date of birth')), '%Y-%m-%d').date() if pd.notna(row.get('Date of birth')) else datetime.datetime.min.date(),
                    last_promotion_date = datetime.datetime.strptime(str(row.get('Last promotion date')), '%Y-%m-%d').date() if pd.notna(row.get('Last promotion date')) else datetime.datetime.min.date(),
                    next_promotion_date = datetime.datetime.strptime(str(row.get('Next promotion date')), '%Y-%m-%d').date() if pd.notna(row.get('Next promotion date')) else datetime.datetime.min.date(),
                    joining_date = datetime.datetime.strptime(str(row.get('Date employed')), '%Y-%m-%d').date() if pd.notna(row.get('Date employed')) else datetime.datetime.min.date(),
                    termination_resignation_date = datetime.datetime.strptime(str(row.get('Date of termination/resignation')), '%Y-%m-%d').date() if pd.notna(row.get('Date of termination/resignation')) else datetime.datetime.min.date(),
                    gender=row.get('Gender'),
                    marital_status=row.get('Marital status'),
                    email=row.get('email address'),
                    address=row.get('Address'),
                    nationality=row.get('Nationality'),
                    state_of_origin=row.get('State of origin'),
                    phone_number=row.get('Phone number'),
                    employee_id= generate_employee_id() if pd.isna(row.get('Employee ID')) else row.get('Employee ID'),
                    department=row.get('Department/division'),
                    job_role=row.get('Job role'),
                    employment_type=row.get('Employment type', 'Full-time'),
                    employment_status=row.get('Employment status', 'Active'),
                    designation=row.get('Designation', 'Employee'),
                    level=row.get('Level'),
                    basic_salary=row.get('Salary')  if pd.notna(row.get('Salary')) else 0,
                    bank_name=row.get('bank name'),
                    account_number=row.get('account number'),
                    account_name=row.get('account name'),
                    pension_id=row.get('pension ID'),
                    tax_id=row.get('tax ID'),
                    emergency_contacts=row.get('Emergency contacts', 'None'),
                    highest_qualification=row.get('Highest qualification'),
                    skills_qualifications=row.get('Skills/qualifications'),
                    next_of_kin_name=row.get('Next of kin name'),
                    next_of_kin_relationship=row.get('Next of kin relationship'),
                    next_of_kin_phone_number=row.get('Next of kin phone number'),
                    branch=branch,
                    adminuser=admin
                )
                employee_ids.append(f"{row.get('Employee ID}')} {row.get('First Name')} {row.get('Last Name')}")
            except Exception as e:
                # Append error message with employee information to the list
                print(e)
                employee_ids.append(f"{row.get('Employee ID')} {row.get('First Name')} {row.get('Last Name')}")
                error_messages.append(f'Error creating employee {row.get("First Name")} {row.get("Last Name")}: {e}')
        
        if error_messages:
            # Return failure message with all error messages
            print(error_messages)
            return {'success': False, 'message': '\n'.join(error_messages)}
        else:
            return {'success': True, 'message': 'All employees created successfully.'}
    
    except Exception as e:
        print(e.with_traceback())
        return {'success': False, 'message': f'Error processing file: {e}'}

# process payroll data
@shared_task
def process_payroll_data(file_content:bytes=None, filename:str=None, branch_id:str = None):
    try:
        if filename.lower().endswith('.xls') or filename.lower().endswith('.xlsx'):
            df = pd.read_excel(BytesIO(file_content))
        elif filename.lower().endswith('.csv'):
            df = pd.read_csv(BytesIO(file_content))
        else:
            # Handle unsupported file formats
            return {'success': False, 'message': 'Unsupported file format.'}
        error_messages = [] # List to store error messages

        # Iterate over the rows in the DataFrame and create payrolls
        for _, row in df.iterrows():
            employee_id = row.get('Employee ID').upper()
            try:
                employee = get_object_or_404(Employee, employee_id=employee_id, branch__branch_id=branch_id)
                payroll = Payroll.objects.create(
                    employee=employee,
                    year=row.get('Year') or datetime.date.year,
                    month=row.get('Month') or datetime.date.month,
                    payment_status=row.get('Payment Status', 'Pending'),
                    housing_allowance=row.get('Housing Allowance', 0),
                    transport_allowance=row.get('Transport Allowance', 0),
                    feeding_allowance=row.get('Feeding Allowance', 0),
                    utility_allowance=row.get('Utility Allowance', 0),
                    other_allowance=row.get('Other Allowance', 0),
                    tax=row.get('Tax', 0),
                    pension=row.get('Pension', 0),
                    loan=row.get('Loan', 0),
                    other_deductions=row.get('Other Deductions', 0),
                    late_penalty=row.get('Late Penalty', 0),
                    absent_penalty=row.get('Absent Penalty', 0),
                    overtime_bonus=row.get('Overtime Bonus', 0),
                    performance_bonus=row.get('Performance Bonus', 0),
                    performance_penalty=row.get('Performance Penalty', 0),
                    basic_salary=row.get('Basic Salary', 0)
                )
                payroll.save()
            except Exception as e:
                # Append error message with employee information to the list
                error_messages.append(f'Error creating payroll for employee with ID {employee_id}: {e}')
        # Return success message
        return {'success': True, 'message': 'Payroll created successfully.'}
    
    except Exception as e:
        # Handle any unexpected errors during file processing
        return {'success': False, 'message': f'Error processing file: {e}'}
