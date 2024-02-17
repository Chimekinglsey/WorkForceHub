import re
from django.shortcuts import render, redirect
import json
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .backends import AdminUserAuthBackend
from django.contrib.auth import login, logout
from employees.models import Employee, AdminUser, PasswordResetToken, Education, WorkHistory,\
      Performance, BankDetails, EmployeeDocs, Payroll, Appointments, Attendance, Leave
from organizations.models import Organization, Branch
from .forms import EmployeeForm, SignUpForm, ProfileUpdateForm, BranchForm
from django.http import JsonResponse, Http404
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime
from django.urls import reverse
import random, string



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
@login_required(login_url='login')
def branch_dashboard(request, branch_id):
    """Branch Dashboard"""
    branch = get_object_or_404(Branch, id=branch_id)
    if branch.organization.admin_user != request.user:
        raise Http404('Branch not found')

    organization = branch.organization
    branches = Branch.objects.filter(organization=organization)
    employees = Employee.objects.filter(branch=branch, is_archived=False)
    archived_employees = Employee.objects.filter(branch=branch, is_archived=True)
    form = EmployeeForm(organization=organization, adminuser=request.user)

    if request.method == 'POST':
        form = EmployeeForm(organization=organization, adminuser=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            print(form.cleaned_data.get('email'))
            messages.success(request, 'Employee created successfully')
            return redirect('branch_dashboard', branch_id=branch.id)
        else:
            messages.error(request, 'Employee creation failed')
            return render(request, 'employees/branch_dashboard.html', {'branch': branch, 'branches': branches, 'employees': employees,
                                                                      'branch_id': branch.id, 'form': form, 'archived_employees': archived_employees})

    return render(request, 'employees/branch_dashboard.html', {'branch': branch, 'branches': branches,
                                                               'employees': employees, 'branch_id': branch.id,
                                                               'form': form, 'archived_employees': archived_employees})


# update employee
@require_POST
def update_employee(request, emp_id):
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
                    'employment_status', 'employment_type', 'designation', 'level', 'salary'
                    ]:
        if field in data and data[field] != '':
            if field == 'email' and employee.email != data[field]:
                try:
                    Employee.objects.get(email=data[field])
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
    return JsonResponse({'type': 'success', 'message': 'Employee record updated successfully'}, status=200)


# Delete employee
@require_POST
def delete_employee(request, emp_id):
    try:
        employee = Employee.objects.get(pk=emp_id)
    except Employee.DoesNotExist:
        return JsonResponse({'error': 'Employee not found'}, status=404)
    employee.delete()
    return JsonResponse({'type': 'success', 'message': 'Employee record deleted successfully'}, status=200)

# archive employee
@require_POST
def archive_employee(request, emp_id):
    try:
        employee = Employee.objects.get(pk=emp_id)
    except Employee.DoesNotExist:
        return JsonResponse({'type': 'error', 'message': 'Employee not found'}, status=404)
    employee.is_archived = True
    employee.archived_at = timezone.now()
    employee.archived_by = request.user.get_full_name()
    employee.archived_reason = request.POST.get('reason')
    employee.employment_status = 'Inactive'
    employee.save()
    messages.success(request, f'Employee {employee.first_name} archived successfully')
    return JsonResponse({'type': 'success', 'message': 'Employee record archived successfully'}, status=200)

# unarchive employee
@require_POST
def unarchive_employee(request, emp_id):
    try:
        employee = Employee.objects.get(pk=emp_id)
    except Employee.DoesNotExist:
        return JsonResponse({'type': 'error', 'message': 'Employee not found'}, status=404)
    employee.is_archived = False
    employee.save()
    messages.success(request, f'Employee {employee.first_name} restored successfully')
    return JsonResponse({'type': 'success', 'message': 'Employee record unarchived successfully'}, status=200)

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