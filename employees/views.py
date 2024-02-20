from atexit import register
from django.shortcuts import render, redirect
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .backends import AdminUserAuthBackend
from django.contrib.auth import login, logout
from employees.models import Employee, AdminUser, PasswordResetToken, Education, WorkHistory,\
      Performance, EmployeeDocs, Payroll, Appointments, Attendance, Leave
from organizations.models import Organization, Branch
from .forms import EmployeeForm, SignUpForm, ProfileUpdateForm, BranchForm
from django.http import JsonResponse, Http404
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime
from django.urls import reverse
import random, string
from statistics import mean
from .forms import PayrollForm

# landing page
def landing_page(request):
    """WorkForceHub HOMEPAGE"""
    if request.user.is_authenticated:
        return render(request, 'employees/landing_page.html', {'user': request.user})
    return render(request, 'employees/landing_page.html', {'user': None})

# signup page
def signup(request):
    """Sign Up Page"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
        elif form.errors:
            messages.error(request, f'Conflict in {list(form.errors)}')
            return render(request, 'employees/signup.html', {'form': form, 'errors': form.errors})
    else:
        form = SignUpForm()
    return render(request, 'employees/signup.html', {'form': form})


def login_view(request):
    """Login page"""
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email').strip()
        password = request.POST.get('password')

        user = AdminUserAuthBackend().authenticate(request, username_or_email=username_or_email, password=password)
        if user is not None:
            login(request, user, backend='employees.backends.AdminUserAuthBackend')  # Authenticate the user
            messages.success(request, 'Login successful')

            if user.employee_id is None:
                return redirect('profile_update')
            return redirect('create_org')
        else:
            messages.error(request, 'Incorrect username or password')
            return redirect('login') 
    return render(request, 'employees/login.html')


@login_required(login_url='login')
def profile_update(request):
    """Update profile"""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('create_org')
    else:
        # Initialize form with instance of the logged-in user
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'employees/profile_update.html', {'form': form})


# create organization DASHBOARD
@login_required(login_url='login')
def org_dashboard(request):
    """Organization Dashboard"""

    form = BranchForm(request.user)
    org = Organization.objects.filter(admin_user=request.user).first()
    branches = Branch.objects.filter(organization=org)
    admin = request.user

    if request.method == 'POST':
        admin_user = get_object_or_404(AdminUser, id=request.user.id)
        org_data = request.POST.dict()
        org_data.pop('csrfmiddlewaretoken')
        # Remove csrfmiddlewaretoken key from the dictionary
        if org:
            for fields in ['name', 'industry', 'sector', 'size', 'branches', 'headquarter', 'website', 'description',
                        'contact_phone', 'contact_email', 'mailing_address', 'revenue', 'profit', 'employee_benefits',
                        'facebook', 'twitter', 'linkedin', 'certifications']:
                if fields in org_data and org_data[fields] != '':
                    setattr(org, fields, org_data[fields])
            org.save()
            messages.success(request, 'Organization updated successfully')
            return render(request, 'employees/org_dashboard.html', {'org': org, 'branches': branches, 'form': form, 'user': admin})
        org = Organization(admin_user=admin_user, **org_data)
        org.save()
        
        messages.success(request, 'Organization created successfully')
        return render(request, 'employees/org_dashboard.html', {'org': org, 'branches': branches, 'form': form, 'user': admin})
    
    return render(request, 'employees/org_dashboard.html', {'form': form, 'org': org, 'branches': branches, 'user': admin})

# create branch of organization
@login_required(login_url='login')
@require_POST
def create_branch(request):
    """Create branch of organization"""
    form = BranchForm(request.user, request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Branch created successfully')
        return JsonResponse({'success': True}, status=status.HTTP_201_CREATED)
    else:
        messages.error(request, 'Branch creation failed')
        return JsonResponse({'success': False, 'error_message': form.errors}, status=status.HTTP_400_BAD_REQUEST)

def parse_date(date_str):
    """Parse a date string in the format yyyy-mm-dd to a date object.

    Returns:
        date: The parsed date object, or the oldest allowed date (`datetime.MINYEAR-1-1`)
             if parsing fails.
    """

    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return datetime.min.date()


# branch dashboard
@login_required(login_url='login')
def branch_dashboard(request, branch_id):
    """Branch Dashboard"""
    branch = get_object_or_404(Branch, id=branch_id)
    if branch.organization.admin_user != request.user or branch.organization is None:
        raise Http404('Branch not found')

    organization = branch.organization
    branches = Branch.objects.filter(organization=organization)
    employees = Employee.objects.filter(branch=branch, is_archived=False)
    archived_employees = Employee.objects.filter(branch=branch, is_archived=True)

    form = EmployeeForm(organization=organization, adminuser=request.user)

    # employee statistics
    total_employees_count = Employee.objects.filter(branch=branch, is_archived=False).count()
    archived_employees_count = Employee.objects.filter(branch=branch, is_archived=True).count()
    active_employees_count = Employee.objects.filter(branch=branch, is_archived=False, employment_status='Active').count()
    inactive_employees_count = Employee.objects.filter(branch=branch, is_archived=False, employment_status='Inactive').count()
    total_employees_on_leave_count = Employee.objects.filter(branch=branch, is_archived=False, employment_status='On Leave').count()
    monthly_created_employees = branch.monthly_created_employees

    # leave statistics
    leave_requests = Leave.objects.filter(employee__branch=branch)
    pending_leave_requests = leave_requests.filter(leave_status='Pending')
    approved_leave_requests = leave_requests.filter(leave_status='Approved').count()
    declined_leave_requests = leave_requests.filter(leave_status='Declined').count()
    active_leave = leave_requests.filter(leave_status='Approved', leave_end_date__gte=timezone.now().date())
    leave_history = leave_requests.filter(leave_status='Approved', leave_end_date__lt=timezone.now())
    leave_durations = [(leave.leave_end_date - leave.leave_start_date).days for leave in leave_history]
    average_leave_duration = mean(leave_durations) if leave_durations else 0

    # payroll statistics
    payroll = Payroll.objects.filter(employee__branch=branch).order_by('-year', '-month')
    total_payroll = payroll.count()
    total_netpay = sum([p.net_pay for p in payroll])
    total_deductions = sum([p.total_deductions for p in payroll])
    total_allowances = sum([p.total_allowance for p in payroll])
    average_netpay = total_netpay / total_payroll if total_payroll else 0
    total_payment = total_netpay + total_allowances


    

    context = {'branch': branch, 'branches': branches, 'employees': employees,'branch_id': branch.id, 'form': form, 
                'archived_employees': archived_employees, 'total_employees_count': total_employees_count,
                'archived_employees_count': archived_employees_count, 'active_employees_count': active_employees_count,
                'inactive_employees_count': inactive_employees_count, 'active_leave': active_leave,
                'total_employees_on_leave_count': total_employees_on_leave_count, 'monthly_created_employees': monthly_created_employees,
                'pending_leave_requests': pending_leave_requests, 'approved_leave_requests': approved_leave_requests,
                'declined_leave_requests': declined_leave_requests, 'average_leave_duration': average_leave_duration,
                'leave_requests': leave_requests, 'leave_history': leave_history, 'payroll': payroll,
                'total_payroll': total_payroll, 'total_payment': total_payment, 'total_deductions': total_deductions,
                'total_allowances': total_allowances, 'total_netpay': total_netpay, 'average_salary': average_netpay
              }
    if request.method == 'POST':
        form = EmployeeForm(organization=organization, adminuser=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            employee_id = request.POST.get('employee_id')
            existing_employee = Employee.objects.filter(employee_id=employee_id, branch=branch).first()
            if existing_employee:
                messages.error(request, 'Employee with this ID already exists')
                return render(request, 'employees/branch_dashboard.html', context=context)
            else:
                form.save()
                messages.success(request, 'Employee created successfully')
                return redirect('branch_dashboard', branch_id=branch.id)
        else:
            messages.error(request, 'Employee creation failed')
            return render(request, 'employees/branch_dashboard.html', context=context)    
    return render(request, 'employees/branch_dashboard.html', context=context)

# update employee
@require_POST
def update_employee(request, emp_id):
    """Update employee record"""
    data = request.POST.dict()
    try:
        employee = Employee.objects.get(pk=emp_id)
    except Employee.DoesNotExist:
        return JsonResponse({'error': 'Employee not found'}, status=404)

    for field in ['first_name', 'middle_name', 'last_name', 'phone_number',
                    'dob', 'gender', 'marital_status', 'address', 'nationality', 'state_of_origin',
                    'email', 'employee_id', 'branch', 'department', 'job_role', 'last_promotion_date', "next_promotion_date",
                    'joining_date', 'next_of_kin_name', 'next_of_kin_relationship', 'next_of_kin_phone_number', 
                    'next_of_kin_address', 'emergency_contacts', 'highest_qualification', 
                    'skills_qualifications', 'employment_status', 'employment_type', 'designation',
                    'employment_status', 'employment_type', 'designation', 'level', 'salary', 'account_number', 'bank_name',
                    'account_name', 'pension_id', 'tax_id'
                    ]:
        if field in data and data[field] != '':
            if field == 'email' and employee.email != data[field]:
                try:
                    Employee.objects.get(email=data[field])
                    messages.error(request, 'Employee with this email already exists')
                    return JsonResponse({'type': 'error', 'message': 'Employee with this email already exists'}, status=400)
                except Employee.DoesNotExist:
                    pass
            setattr(employee, field, data[field])
        for field in ['profile_picture', 'employment_letter', 'highest_certificate']:
            if field in request.FILES:
                existing_file = getattr(employee, field)
                if existing_file:
                    existing_file.delete()
                setattr(employee, field, request.FILES[field])
    employee.save()
    messages.success(request, 'Record updated successfully')
    return JsonResponse({'type': 'success', 'message': 'Record updated successfully'}, status=200)


# Leave request
@require_POST
def leave_request(request):
    """Employee leave request"""
    data = request.POST.dict()
    try:
        branch = Branch.objects.get(pk=data['branch_id'])
        employee = Employee.objects.filter(employee_id=data['employee_id'].strip(), branch=branch).first()
    except Employee.DoesNotExist:
        messages.error(request, "Employee not found")
        return redirect('branch_dashboard', branch_id=branch.id)
    leave = Leave(employee=employee, leave_type=data['leave_type'], leave_start_date=parse_date(data['start_date']),
                   leave_end_date=parse_date(data['end_date']), leave_reason=data['reason'])
    leave.save()
    messages.success(request, f"Leave request submitted successfully")
    return redirect('branch_dashboard', branch_id=branch.id)

# Accept and decline leave request
@csrf_exempt
@require_POST
def manage_leave_request(request, leave_id):
    """Accept or decline leave request"""
    leave = get_object_or_404(Leave, pk=leave_id)
    if not leave:
        messages.error(request, "Leave request not found")
        return JsonResponse({'error': 'Leave request not found'}, status=404)
    action = request.POST.get('action')
    if action == 'accept':
        leave.leave_status = 'Approved'
        leave.save()
        messages.success(request, 'Leave request accepted')
    elif action == 'decline':
        leave.leave_status = 'Declined'
        leave.save()
        messages.success(request, 'Leave request declined')
    return redirect('branch_dashboard', branch_id=leave.employee.branch.id)


# Delete employee
@login_required
def delete_employee(request, emp_id):
    try:
        employee = Employee.objects.get(pk=emp_id)
        id = employee.employee_id
    except Employee.DoesNotExist:
        messages.error(request, "Employee not found")
        return JsonResponse({'error': 'Employee not found'}, status=404)
    employee.delete()
    messages.success(request, f" Employee {id} deleted successfully")
    return JsonResponse({'type': 'success', 'message': f'Employee {id} deleted successfully'}, status=200)


# archive employee
@require_POST
def archive_employee(request, emp_id):
    try:
        employee = Employee.objects.get(pk=emp_id)
    except Employee.DoesNotExist:
        messages.error(request, "Employee not found")
        return JsonResponse({'type': 'error', 'message': 'Employee not found'}, status=404)
    employee.is_archived = True
    employee.archived_at = timezone.now()
    employee.archived_by = request.user.get_full_name()
    employee.archived_reason = request.POST.get('reason')
    employee.employment_status = 'Inactive'
    employee.save()
    messages.success(request, f'Employee {employee.employee_id} archived successfully')
    return JsonResponse({'type': 'success', 'message': 'Employee record archived successfully'}, status=200)


# unarchive employee
@login_required
def restore_archive(request, emp_id):
    try:
        employee = Employee.objects.get(pk=emp_id)
    except Employee.DoesNotExist:
        messages.error(request, "Employee not found")
        return JsonResponse({'type': 'error', 'message': 'Employee not found'}, status=404)
    employee.is_archived = False
    employee.archived_at = None
    employee.archived_by = None
    employee.archived_reason = None
    employee.employment_status = 'Active'
    employee.save()
    messages.success(request, f'Employee {employee.employee_id} restored successfully')
    return JsonResponse({'type': 'success', 'message': 'Employee record unarchived successfully'}, status=200)








"""Payroll Management"""
@require_POST
def create_payroll(request):
    """Create payroll for an employee"""
    data = request.POST.dict()
    print(data)
    try:
        employee = Employee.objects.get(pk=data['employee_id'])
        employee.basic_salary = int(data['basic_salary'])
        employee.save()
    except Employee.DoesNotExist:
        messages.error(request, "Employee not found")
        return JsonResponse({'error': 'Employee not found'}, status=404)
    # check if payroll already exists for the employee
    existing_payroll = Payroll.objects.filter(employee=employee, year=data['year'], month=data['month']).first()
    if existing_payroll:
        messages.error(request, "Payroll already exists for this employee, update or delete existing payroll first")
        return JsonResponse({'error': 'Payroll already exists for this employee, update or delete existing payroll first'}, status=400)
    payroll = Payroll(employee=employee, year=(data['year']), month=data['month'], payment_status=data['payment_status'],
                        housing_allowance=int(data['housing_allowance']), transport_allowance=int(data['transport_allowance']),
                        feeding_allowance=int(data['feeding_allowance']), utility_allowance=int(data['utility_allowance']),
                        other_allowance=int(data['other_allowance']), tax=int(data['tax']), pension=int(data['pension']),
                        loan=int(data['loan']), other_deductions=int(data['other_deductions']),
                        late_penalty=int(data['late_penalty']), absent_penalty=int(data['absent_penalty']), 
                        overtime_bonus=int(data['overtime_bonus']), performance_bonus=int(data['performance_bonus']), 
                        performance_penalty=int(data['performance_penalty'])
                      )
    payroll.save()
    messages.success(request, f"Payroll created successfully")
    return redirect('payroll_detail', payroll_id=payroll.id)

# health_insurance=int(data['health_insurance']),


def update_payroll(request, payroll_id):
    """Update payroll"""
    payroll = get_object_or_404(Payroll, id=payroll_id)
    if request.method == 'POST':
        form = PayrollForm(request.POST, instance=payroll)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payroll updated successfully')
            return redirect('payroll_detail', payroll_id=payroll_id)
        else:
            messages.error(request, f'{list(form.errors)}Payroll update failed')
            return render(request, 'payroll/update_payroll.html', {'form': form})
    else:
        form = PayrollForm(instance=payroll)
    return render(request, 'payroll/update_payroll.html', {'form': form})

def payroll_detail(request, payroll_id):
    """Payroll detail"""
    payroll = get_object_or_404(Payroll, id=payroll_id)
    return render(request, 'payroll/payroll_detail.html', {'payroll': payroll})

def payroll_list(request):
    """List of payrolls"""
    payrolls = Payroll.objects.all()
    return render(request, 'payroll/payroll_list.html', {'payrolls': payrolls})

def payroll_history(request, emp_id):
    employee = get_object_or_404(Employee, id=emp_id)
    payroll_history = Payroll.objects.filter(employee=employee).order_by('-year', '-month')
    
    context = {
        'employee': employee,
        'payroll_history': payroll_history
    }
    return render(request, 'payroll/payroll_history.html', context)

def delete_payroll(request, payroll_id):
    """Delete payroll"""
    payroll = get_object_or_404(Payroll, id=payroll_id)
    payroll.delete()
    messages.success(request, f'Payroll deleted successfully')
    return redirect('branch_dashboard', branch_id=payroll.employee.branch.id)














# statistics for an employee
@login_required
def employee_statistics(request, emp_id):
    try:
        employee = Employee.objects.get(pk=emp_id)
    except Employee.DoesNotExist:
        messages.error(request, "Employee not found")
        return JsonResponse({'type': 'error', 'message': 'Employee not found'}, status=404)
    performance = Performance.objects.filter(employee=employee)
    education = Education.objects.filter(employee=employee)
    work_history = WorkHistory.objects.filter(employee=employee)
    employee_docs = EmployeeDocs.objects.filter(employee=employee)
    payroll = Payroll.objects.filter(employee=employee)
    appointments = Appointments.objects.filter(employee=employee)
    attendance = Attendance.objects.filter(employee=employee)
    leave = Leave.objects.filter(employee=employee)
    return render(request, 'employees/employee_statistics.html', {'employee': employee, 'performance': performance,
                                                                 'education': education, 'work_history': work_history,
                                                                 'employee_docs': employee_docs,
                                                                 'payroll': payroll, 'appointments': appointments,
                                                                 'attendance': attendance, 'leave': leave})


# Forgot Password
def forgot_password(request):
    """Forgot Password"""
    if request.method == 'POST':
        sender = request.POST.get('sender')
        recipient = request.POST.get('email').strip()
        subject = "Password Reset Code"
        token = generate_password_reset_token()
        user = get_object_or_404(AdminUser, email=recipient)
        if user:
            # Use get_or_create to create a new PasswordResetToken if it doesn't exist
            password_reset_token, created = PasswordResetToken.objects.get_or_create(user=user)
            password_reset_token.token = token
            password_reset_token.created_at = timezone.now()  # Update the created_at field
            password_reset_token.save()

            message = f"Your password reset code is {token} (expires in one hour).\n\nPlease do not share this code with anyone\nIf you didn't request this pin, we recommend you change your WorkForceHub password.\n\nRegards, \nKingsley, WorkForceHub Team"
            try:
                send_mail(subject, message, sender, [recipient])
                response_data = {'success': True}
            except Exception as e:
                response_data = {'success': False, 'error_message': str(e)}
            return JsonResponse(response_data)
        else:
            messages.error(request, 'User does not exist')
            return JsonResponse({'success': False, 'error_message': 'User does not exist'})
    return render(request, 'user/user_login.html', context={'user_email': recipient})


# Genereate password reset token
def generate_password_reset_token():
    """Generate password reset token"""
    first_digit = random.choice(string.digits[1:])
    rest_of_digits = ''.join(random.choices(string.digits, k=5))
    token = first_digit + rest_of_digits
    return int(token)


#confirm password reset token
def confirm_password_reset_token(request):
    """Confirm password reset token"""
    if request.method == 'POST':
        token = request.POST.get('token')
        user_email = request.POST.get('user_email')
        user = get_object_or_404(AdminUser, email=user_email)
        
        try:
            password_reset_token = PasswordResetToken.objects.get(user=user)
        except PasswordResetToken.DoesNotExist:
            return JsonResponse({'success': False, 'error_message': 'Token not found'})

        # Check if the provided token matches and is not expired
        if token == password_reset_token.token and not password_reset_token.is_expired():
            # Token is valid, you can proceed with the next steps
            return JsonResponse({'success': True})
        else:
            messages.error(request, 'Invalid or expired token')
            return JsonResponse({'success': False, 'error_message': 'Invalid or expired token'})

    return JsonResponse({'success': False})


# reset password
def reset_password(request):
    """Reset Password"""
    if request.method == 'POST':
        password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmPassword')
        email = request.POST.get('user_email').strip()
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return JsonResponse({'success': False, 'error_message': 'Passwords do not match'})
        try:
            user = get_object_or_404(AdminUser, email=email)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful, Please Login')
            return JsonResponse({'success': True, 'redirect_url': reverse('login')})
        except AdminUser.DoesNotExist:
            messages.error(request, 'User does not exist')
            return JsonResponse({'success': False, 'error_message': 'User does not exist'})
    return render(request, 'employee/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You Logged Out")
    return redirect('login') 