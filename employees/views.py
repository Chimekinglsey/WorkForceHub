"""View Function for workforcehub"""
import os
from django.shortcuts import render, redirect
from functools import wraps
from django.core.exceptions import PermissionDenied
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from .backends import AdminUserAuthBackend
from django.contrib.auth import login, logout
from employees.models import Employee, AdminUser, PasswordResetToken, Education, WorkHistory,\
    Performance, EmployeeDocs, Payroll, Appointments, Attendance, Leave, Finance
from organizations.models import Organization, Branch, Transfer, Report
from .forms import DetailedFinanceForm, EmployeeForm, SignUpForm, ProfileUpdateForm, BranchForm, PayrollForm
from .forms import  PerformanceReviewForm, DelegateAdminCreationForm, ReportForm, BasicFinanceForm
from .forms import UserProfileForm, ChangePasswordForm, BranchDocumentsForm, TransferForm, Picture_update, EmpDpForm,\
    PayrollUploadForm
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime
import random, string
from statistics import mean
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from .forms import EmployeesUploadForm
from employees.celery.tasks import process_employee_data, generate_employee_id, send_password_reset_email,\
    send_welcome_mail, process_payroll_data
from .tests.tarsk import test_errors



def resize_image(image):
    """Resize the given image if necessary"""
    try:
        img = Image.open(image)
        
        # Check if the image dimensions are within the desired size, resize it if not
        max_width, max_height = 300, 300
        if img.width <= max_width and img.height <= max_height:
            return image
        img.thumbnail((max_width, max_height))
        
        # Convert the resized image back to BytesIO for saving
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        # Create an InMemoryUploadedFile object from the resized image data
        return InMemoryUploadedFile(img_io, None, image.name, 'image/png', img_io.tell(), None)
    except Exception as e:
        print(f"Error resizing image: {e}")
        return None



"""Helper Functions"""
def generate_org_id():
    """Generate 10 digits and 2 uppercase organization ID"""
    while True:
        org_id = ''.join(random.choices(string.digits, k=8)) + ''.join(random.choices(string.ascii_uppercase, k=2))
        # Check if the first character is not zero
        if org_id[0] != '0' and not Organization.objects.filter(org_id=org_id).exists():
            return org_id

def generate_branch_id():
    """Generate 5 digits branch ID"""
    while True:
        branch_id = ''.join(random.choices(string.digits, k=5))
        # Check if the first character is not zero
        if branch_id[0] != '0' and not Branch.objects.filter(branch_id=branch_id).exists():
            return branch_id
       
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

def mask_password(pwd:str, mask_char:str='*'):
  """Masks a password by replacing all characters except the first and last two with asterisks.

  Args:
      pwd: The password string to be masked. Form validation ensures pwd is at least 8 chars long
      mask_char: The character to use for masking (defaults to asterisk '*').

  Returns:
      The masked password string.
  """
  if len(pwd) >= 8:
    return pwd[:2] + mask_char * (len(pwd) - 4) + pwd[-2:]

def superuser_required(view_func):
    """Decorator to check if the user is a superuser"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            error_message = 'You are not authorized to perform this operation'
            return render(request, 'delegates/access_denied.html', {'error_message': error_message})
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def delegate_required(view_func):
    """ 
        Verifies that the user has permission perform the intended operation
        *emp_id:* unique id of the employee
        *employee:* A None instance of Employee Model that will be passed back to the function after db call
    
    """
    @wraps(view_func)
    def wrapper(request, emp_id, *args, **kwargs):
        employee = get_object_or_404(Employee, employee_id=emp_id)
        if employee.branch.organization != request.user.branch.organization:
            raise PermissionDenied('You are not allowed to perform this operation')
        if request.user.is_delegate and request.user.branch != employee.branch:
            raise PermissionDenied('You are not allowed to perform this operation')
        return view_func(request, emp_id, employee=employee, *args, **kwargs)
    return wrapper

"""Helper Functions ends here"""


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
            pwd=form.cleaned_data['password1']
            pwd = mask_password(pwd)
            user = form.save()
            send_welcome_mail.delay(recipient=user.email,
                                     email=user.email,
                                     pwd=pwd,
                                     username=user.username,
                                     )
            messages.success(request, 'Account created successfully, Please login to continue.')
            return redirect('login')
        elif form.errors:
            last_error = form.errors[list(form.errors.keys())[-1]][-1]
            messages.error(request, last_error)
            return render(request, 'employees/signup.html', {'form': form, 'errors': form.errors})
    else:
        form = SignUpForm(data=request.POST or None)
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
            
            if user.is_superuser and user.employment_status != 'Suspended' and  not user.first_name:
                return redirect('profile_update')
            
            if user.employment_status == 'Suspended':
                messages.error(request, 'Your account has been suspended, contact the admin for more information')
                error_message = 'Your account has been suspended, contact the admin for more information'
                return render(request, 'delegate/access_denied.html', error_message=error_message)
            
            if user.is_delegate:
                return redirect('branch_dashboard', branch_id=user.branch.branch_id)

            return redirect('org_dashboard')
        else:
            messages.error(request, 'Incorrect username or password')
            return render(request, 'employees/login.html', {'username_or_email': username_or_email})
    return render(request, 'employees/login.html')


@login_required(login_url='login')
def profile_update(request):
    """Update profile"""
    if request.user.is_delegate:
        messages.error(request, 'You do not have permission to access this page')
        return redirect('branch_dashboard', branch_id=request.user.branch.branch_id)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES or None, instance=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            if 'profile_picture' in request.FILES:
                resized_image = resize_image(request.FILES['profile_picture'])
                instance.profile_picture = resized_image
            if not request.user.branch:
                instance.adminuser = request.user
            instance.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('org_dashboard')
    elif request.user.employee_id:
        form = ProfileUpdateForm(instance=request.user, initial={'profile_picture':None})
    else:
        # Initialize form with instance of the logged-in user
        form = ProfileUpdateForm(initial={'employee_id': generate_employee_id()})#data=request.POST or None
    return render(request, 'employees/profile_update.html', {'form': form})



"""Organization Management and Branch Creation"""
# create organization DASHBOARD
@login_required(login_url='login')
# @superuser_required
def org_dashboard(request):
    """Organization Dashboard"""
    # Use select_related to fetch related admin_user in a single query
    user = request.user
    if not user.first_name:
        return redirect('profile_update')

    org = Organization.objects.select_related('admin_user').filter(admin_user=request.user.adminuser).first()

    form = BranchForm(request.user, data=request.POST or None)
    branches = Branch.objects.filter(organization=org)
    admin = request.user

    # Get all delegate admins associated with the organization outside the current user
    all_admin = AdminUser.objects.filter(branch__organization=org)
    delegate_admins = all_admin.filter(is_delegate=True, is_superuser=False)
    superusers = all_admin.filter(is_superuser=True)
    delegate_admin_form = DelegateAdminCreationForm(organization=org, adminuser=admin, data=request.POST or None)

    change_password_form = ChangePasswordForm(request.user, data=request.POST or None)
    profile_update_form = ProfileUpdateForm(instance=request.user, initial={'profile_picture': None})

    reports = Report.objects.filter(branch__organization=org)

    # Transfer Statistics
    transfers = Transfer.objects.filter(organization=org)
    pending_transfers = transfers.filter(status='Pending')
    approved_transfers = transfers.filter(status='Approved')
    declined_transfers = transfers.filter(status='Declined')
    
    # Count transfers using annotations
    monthly_transfer_count = transfers.filter(created_at__month=timezone.now().month).count()
    last_month_transfer_count = transfers.filter(created_at__month=timezone.now().month - 1).count()
    
    employees = Employee.objects.filter(branch__organization=org)

    context = {
        'form': form, 'org': org, 'branches': branches, 'user': admin,
        'delegate_admin_form': delegate_admin_form,'delegate_admins': delegate_admins,
        'transfers': transfers, 'pending_transfers': pending_transfers,
        'approved_transfers': approved_transfers, 'declined_transfers': declined_transfers,
        'monthly_transfer_count': monthly_transfer_count, 
        'last_month_transfer_count': last_month_transfer_count,
        'employees': employees, 'reports': reports,
        'admin_password_form': change_password_form,
        'superusers': superusers, 'profile_update_form': profile_update_form
    }
    return render(request, 'employees/org_dashboard.html', context=context)


# create update org
@login_required
@require_POST
@superuser_required
def create_update_org(request):
    """ Creates an new organization, updates an existing organization"""
    admin = get_object_or_404(AdminUser, pk=request.user.pk)
    org = Organization.objects.filter(admin_user=admin).first()
    org_data = request.POST.dict()
    org_data.pop('csrfmiddlewaretoken', None)  # Remove csrfmiddlewaretoken key from the dictionary
    org_data['admin_user'] = request.user.adminuser
    org_data['name'] = org_data['name'].upper()

    if org:
        for field in ['name', 'industry', 'sector', 'size', 'branches', 'headquarter', 'website',
                        'description', 'contact_phone', 'contact_email', 'mailing_address', 'revenue',
                        'profit', 'employee_benefits', 'facebook', 'twitter', 'linkedin', 'certifications']:
            if field in org_data and org_data[field] != '':
                setattr(org, field, org_data[field])
        org.org_id = generate_org_id()
        org.save()
        messages.success(request, 'Organization updated successfully')
    else:
        org = Organization(**org_data)
        org.org_id = generate_org_id()
        admin.is_master_admin = True
        admin.save()
        org.save()
        messages.success(request, 'Organization created successfully')
    return redirect('org_dashboard')


# update admin profile picture

@login_required
@csrf_exempt
@require_POST
def update_dp(request):
    """Updates user profile picture. Delete previous photo to manage disk space efficiently"""
    user = get_object_or_404(AdminUser, pk=request.user.pk)
    # Fetch existing profile picture path # S3 does not support absolute path
    # existing_path = user.profile_picture.path if user.profile_picture else None
    # old_dp_path = existing_path    
    form = Picture_update(request.POST, request.FILES, instance=user)
    if form.is_valid():
        instance = form.save(commit=False)
        
        # Check if profile picture has changed
        if 'profile_picture' in request.FILES:
            profile_picture = request.FILES['profile_picture']
            resized_image = resize_image(profile_picture)
            
            # Replace the profile picture with the resized image
            instance.profile_picture = resized_image
        
        instance.save()
        # # Remove the old profile picture file from the file system. using.delete() was problematic at the moment
        # if (old_dp_path and not 'default' in str(old_dp_path) and
        #     instance.profile_picture and old_dp_path != instance.profile_picture.path): # don't remove the default_profile_picture used by all Employees and Admin
        #     try:
        #         os.remove(old_dp_path)
        #     except OSError as e:
        #         print(f"Error removing old profile picture: {e}")
        
        messages.success(request, 'Profile picture updated successfully')
        return JsonResponse({'success': True, 'profile_picture': instance.profile_picture.url}, status=201)
    else:
        messages.error(request, 'Invalid form data')
        return JsonResponse({'success': False, 'message': 'Error'}, status=405)


# update employee profile picture -> because the form is AdminUser model, we need a new view. 
# TODO: use same form and view for this -> look up multi-model form
@login_required
@csrf_exempt
@require_POST
def update_emp_dp(request, emp_id=None):
    """Updates user profile picture. Delete previous photo to manage disk space efficiently"""
    user = get_object_or_404(Employee, employee_id=emp_id)
    # Fetch existing profile picture path
    # existing_path = user.profile_picture.path if user.profile_picture else None
    # old_dp_path = existing_path
    
    form = EmpDpForm(request.POST, request.FILES, instance=user)
    if form.is_valid():
        instance = form.save(commit=False)
        
        # Check if profile picture has changed
        if 'profile_picture' in request.FILES:
            profile_picture = request.FILES['profile_picture']
            resized_image = resize_image(profile_picture)
            
            # Replace the profile picture with the resized image
            instance.profile_picture = resized_image
        
        instance.save()
        # Remove the old profile picture file from the file system. using.delete() was problematic at the moment
        # if (old_dp_path and not 'default' in str(old_dp_path) and
        #     instance.profile_picture and old_dp_path != instance.profile_picture.path): # don't remove the default_profile_picture used by all Employees and Admin
        #     try:
        #         os.remove(old_dp_path)
        #     except OSError as e:
        #         print(f"Error removing old profile picture: {e}")
        
        messages.success(request, 'Profile picture updated successfully')
        return JsonResponse({'success': True, 'profile_picture': instance.profile_picture.url}, status=201)
    else:
        messages.error(request, 'Invalid form data')
        return JsonResponse({'success': False, 'message': 'Error'}, status=405)



# delete organization
@login_required(login_url='login')
@csrf_exempt
@require_POST
def delete_organization(request, org_id):
    """Delete organization"""
    # Authorization check. Only the organization admin can delete the organization
    if not (request.user.is_master_admin and
            request.user.branch.organization.org_id == org_id and
            request.user.branch.organization.admin_user == request.user):
        raise PermissionDenied('You are not authorized to perform this operation')

    # Fetch organization and delete the org or raise 404
    org = get_object_or_404(Organization, org_id=org_id)
    org.delete()
    messages.success(request, 'Organization deleted successfully')
    return JsonResponse({'success': True}, status=200)

# Delete Branch
@login_required(login_url='login')
@csrf_exempt
@require_POST
@superuser_required
def delete_branch(request, branch_id):
    """delete organization branch"""
    branch = get_object_or_404(Branch, branch_id=branch_id)
    branch.delete()
    messages.success(request, 'Branch deleted successfully')
    return JsonResponse({'success': True}, status=200)


# delete delegate
@login_required(login_url='login')
@csrf_exempt
@require_POST
@superuser_required
def delete_delegate(request, delegate_id):
    """Delete delegate admin"""
    delegate = get_object_or_404(AdminUser, id=delegate_id)
    delegate.delete()
    messages.success(request, 'Delegate admin deleted successfully')
    return JsonResponse({'success': True}, status=200)

# update branch
@login_required(login_url='login')
@csrf_exempt
@superuser_required
def update_branch(request, branch_id):
    """Update branch"""
    branch = get_object_or_404(Branch, branch_id=branch_id)    
    form = BranchForm(request.user, instance=branch, data=request.POST or None)
    context = {'form': form, 'branch': branch}
    if request.method == 'POST':
        form = BranchForm(request.user, request.POST, instance=branch)
        if form.is_valid():
            form.save()
            messages.success(request, 'Branch updated successfully')
            return redirect('org_dashboard')
        else:
            messages.error(request, 'Branch update failed')
            return redirect('org_dashboard')
    return render(request, 'branch/update_branch.html', context=context)

# update delegate
@login_required(login_url='login')
@csrf_exempt
@require_POST
@superuser_required
def update_delegate(request, delegate_id):
    """Update delegate admin"""
    delegate = get_object_or_404(AdminUser, id=delegate_id)
    form = DelegateAdminCreationForm(organization=delegate.branch.organization, adminuser=request.user, data=request.POST, instance=delegate)
    if form.is_valid():
        form.save()
        messages.success(request, 'Delegate admin updated successfully')
        return JsonResponse({'success': True}, status=status.HTTP_201_CREATED)
    else:
        messages.error(request, 'Delegate admin update failed')
        return JsonResponse({'success': False}, status=status.HTTP_400_BAD_REQUEST)

# suspend delegate
@login_required(login_url='login')
@csrf_exempt
@require_POST
@superuser_required
def suspend_delegate(request, delegate_id):
    """Suspend delegate admin"""
    delegate = get_object_or_404(AdminUser, id=delegate_id)
    delegate.is_active = False
    delegate.employment_status = 'Suspended'
    delegate.save()
    messages.success(request, 'Delegate admin suspended successfully')
    return JsonResponse({'success': True}, status=status.HTTP_201_CREATED)


# unsuspend delegate
@login_required(login_url='login')
@csrf_exempt
@require_POST
@superuser_required
def activate_delegate(request, delegate_id):
    """Unsuspend delegate admin"""
    delegate = get_object_or_404(AdminUser, id=delegate_id)
    delegate.is_active = True
    delegate.employment_status = 'Active'
    delegate.save()
    messages.success(request, 'Delegate admin now active!')
    return JsonResponse({'success': True}, status=status.HTTP_201_CREATED)


# create delegate admin
@login_required(login_url='login')
@require_POST
@superuser_required
def create_delegate(request):
    """Create delegate admin"""
    org = Organization.objects.filter(id=request.user.branch.organization.id).first()
    form = DelegateAdminCreationForm(data=request.POST, adminuser=request.user, organization=org)

    if form.is_valid():
        form.save()
        messages.success(request, 'Delegate admin created successfully')
        return JsonResponse({'success': True}, status=status.HTTP_201_CREATED)
    else:
        # If form validation fails, return errors in JSON response
        last_error = form.errors[list(form.errors.keys())[-1]][-1]
        messages.error(request, f'Error occurred: {last_error}')
        return JsonResponse({'success': False}, status=200)


# create branch of organization
@login_required(login_url='login')
@require_POST
@superuser_required
def create_branch(request):
    """Create branch of organization"""
    org = Organization.objects.filter(admin_user=request.user.adminuser).first()
    form = BranchForm(request.user, request.POST)
    branch_names = [b.name for b in org.organization_branches.all()]
    try:
        if form.is_valid() and form.cleaned_data['name'] not in branch_names:
            branch = form.save(commit=False)
            branch.name = branch.name.capitalize()
            branch.branch_id = generate_branch_id()
            branch.organization = org
            branch.save()
            superuser = AdminUser.objects.get(pk=request.user.pk)
            if not superuser.branch:
                superuser.branch = branch
                superuser.save()
            messages.success(request, 'Branch created successfully')
            return JsonResponse({'success': True}, status=status.HTTP_201_CREATED)
        else:
            messages.error(request, 'Invalid form data. Branch with this name may already exists')
            return JsonResponse({'success': False}, status=200)
    except Exception as e:
        messages.error(request, f'Error occurred: {str(e)}')
        return JsonResponse({'success': False}, status=200)
    

"""Branch Management and Employee Creation"""
# branch dashboard
@login_required(login_url='login')
def branch_dashboard(request, branch_id:str):
    """Branch Dashboard"""
    # testing = test_errors.delay(branch_id=branch_id, user_id=request.user.id)
    # testing.get()
    # print(testing.result)

    branch = get_object_or_404(Branch, branch_id=branch_id)
    user = get_object_or_404(AdminUser, pk=request.user.pk)
    if user.branch.branch_id != branch_id and user.branch.organization != branch.organization:
        raise PermissionDenied('You are not allowed to perform this operation')
    
    # delegate admin can only view their branch dashboard
    if request.user.is_delegate:
        if request.user.branch.branch_id != branch_id:
            return render(request, 'delegates/access_denied.html', {'error_message': 'You do not have permission to access this page'})

    organization = branch.organization
    branches = Branch.objects.filter(organization=organization)
    employees = Employee.objects.filter(branch=branch)
    archived_employees = employees.filter(is_archived=True)
    transfers = Transfer.objects.filter(requested_by=request.user)
    today = timezone.now().date()

    # forms
    form = EmployeeForm(initial={'branch': branch, 'adminuser': request.user}, data=request.POST or None, files=request.FILES or None)
    profile_form = UserProfileForm(instance=request.user, data=request.POST or None, files=request.FILES or None)
    change_password_form = ChangePasswordForm(request.user, data=request.POST or None)
    branch_documents_form = BranchDocumentsForm(data=request.POST or None, files=request.FILES or None)
    transfer_form = TransferForm(organization=organization, adminuser=request.user, initial={'source_branch': branch}, data=request.POST or None)
    employees_upload_form = EmployeesUploadForm()
    payroll_upload_form = PayrollUploadForm()

    # employee statistics
    total_employees_count = employees.count()
    archived_employees_count = employees.filter(is_archived=True).count()
    active_employees_count = employees.filter(is_archived=False, employment_status='Active').count()
    inactive_employees_count = employees.exclude(employment_status='Active').count()
    total_employees_on_leave_count = employees.filter(is_archived=False, employment_status='On Leave').count()
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
    total_payment = total_netpay

    # performance statistics
    performance = Performance.objects.filter(employee__branch=branch)
    underperforming_employees = Performance.objects.filter(employee__branch=branch, performance_rating__lt=60)
    average_performance_rating = mean([p.performance_rating for p in performance]) if performance else 0
    high_performers = performance.filter(performance_rating__gte=80)
    improvement_rate = (high_performers.count() / performance.count()) * 100 if performance else 0
    highest_rating = performance.order_by('-performance_rating').first()
    employee_engagement = 'High' if average_performance_rating >= 70 else 'Low'


    # transfer statistics
    pending_transfers = transfers.filter(status='Pending')
    approved_transfers = transfers.filter(status='Approved')
    declined_transfers = transfers.filter(status='Declined')
    transfer_history = transfers.filter(status='Approved')
    incoming_transfers_count = Transfer.objects.filter(destination_branch=branch, status='Approved').count()
    outgoing_transfers_count = Transfer.objects.filter(source_branch=branch, status='Approved').count()


    context = {'branch': branch, 'branches': branches, 'employees': employees,'branch_id': branch.branch_id, 'form': form, 
                'archived_employees': archived_employees, 'total_employees_count': total_employees_count,
                'archived_employees_count': archived_employees_count, 'active_employees_count': active_employees_count,
                'inactive_employees_count': inactive_employees_count, 'active_leave': active_leave,
                'total_employees_on_leave_count': total_employees_on_leave_count, 'monthly_created_employees': monthly_created_employees,
                'pending_leave_requests': pending_leave_requests, 'approved_leave_requests': approved_leave_requests,
                'declined_leave_requests': declined_leave_requests, 'average_leave_duration': average_leave_duration,
                'leave_requests': leave_requests, 'leave_history': leave_history, 'payroll': payroll,
                'total_payroll': total_payroll, 'total_payment': total_payment, 'total_deductions': total_deductions,
                'total_allowances': total_allowances, 'total_netpay': total_netpay, 'average_salary': average_netpay,
                'performance': performance, 'underperformance': underperforming_employees, 'average_performance_rating': average_performance_rating,
                'high_performers': high_performers, 'improvement_rate': improvement_rate, 'highest_rating': highest_rating,
                'employee_engagement': employee_engagement, 'profile_form': profile_form, 'change_password_form': change_password_form,
                'branch_documents_form': branch_documents_form, 'transfer_form': transfer_form, 'transfers': transfers,
                'pending_transfers': pending_transfers, 'approved_transfers': approved_transfers, 'declined_transfers': declined_transfers,
                'transfer_history': transfer_history, 'incoming_transfers_count': incoming_transfers_count, 'outgoing_transfers_count': outgoing_transfers_count,
                'organization': organization, 'today': today, 'employees_upload_form': employees_upload_form, 'payroll_upload_form': payroll_upload_form,
              } 
    return render(request, 'employees/branch_dashboard.html', context=context)


"""Employee Management"""
@login_required
@require_POST
def create_employee(request, branch_id:str):
    """Creates a new employee"""
    branch = get_object_or_404(Branch, branch_id=branch_id)
    if branch.organization != request.user.branch.organization:
        raise PermissionDenied('You are not allowed to perform this operation')
    if request.user.is_delegate and request.user.branch != branch:
        raise PermissionDenied('You are not allowed to perform this operation')

    form = EmployeeForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        employee_id = request.POST.get('employee_id')
        existing_employee = Employee.objects.filter(employee_id=employee_id, branch=branch).first()
        if existing_employee:
            messages.error(request, 'Employee with this ID already exists')
            return JsonResponse({'success': False}, status=200)
        else:
            form.save(commit=False)
                    # Check if profile picture has changed
            if 'profile_picture' in request.FILES:
                profile_picture = request.FILES['profile_picture']
                resized_image = resize_image(profile_picture)
                form.instance.profile_picture = resized_image
            
            # Replace the profile picture with the resized image
            form.instance.branch = branch
            form.instance.adminuser = request.user
            form.save()
            messages.success(request, 'Employee created successfully')
            return redirect('branch_dashboard', branch_id=branch.branch_id)
    else:
        last_error = form.errors[list(form.errors.keys())[-1]][-1]
        messages.error(request, f'Error occurred: {last_error}')
        return redirect('branch_dashboard', branch_id=branch.branch_id)


@require_POST
@login_required
@delegate_required
def update_employee(request, emp_id: str, employee: Employee = None):
    """ Dynamically updates an existing employee data """
    # Employee object is fetched in @delegate_required and passed to functions it decorates
    # Extract data from POST request
    data = request.POST.dict()

    # Update employee fields based on data from request
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
                # Check if email already exists for another employee
                if Employee.objects.filter(email=data[field]).exclude(employee_id=emp_id).exists():
                    messages.error(request, 'Employee with this email already exists')
                    return JsonResponse({'success': False}, status=200)
            setattr(employee, field, data[field])

    # Handle file uploads
    for field in ['profile_picture', 'employment_letter', 'highest_certificate']:
        if field in request.FILES:
            # Get the uploaded file
            uploaded_file = request.FILES[field]
            if uploaded_file and uploaded_file.size > 0:  # Ensure the file is not empty and delete existing file (if any)
                existing_file = getattr(employee, field)
                if existing_file:
                    existing_file.delete()
                if field == 'profile_picture':
                    uploaded_file = resize_image(request.FILES[field])
                setattr(employee, field, uploaded_file)

    employee.save()
    messages.success(request, 'Record updated successfully')
    return JsonResponse({'success': True}, status=200)

# archive employee
@require_POST
@login_required
@delegate_required
def archive_employee(request, emp_id: str, employee: Employee = None):
    """Archives an employee from the organizations branch. Raises error if no employee with the given id is found"""
    employee.is_archived = True
    employee.archived_at = timezone.now()
    employee.archived_by = request.user.get_full_name()
    employee.archived_reason = request.POST.get('reason')
    employee.employment_status='Inactive'
    employee.save()
    messages.success(request, f'Employee {employee.employee_id} archived successfully')
    return JsonResponse({'success': True}, status=200)

# unarchive employee
@login_required
@delegate_required
def restore_archive(request, emp_id: str, employee: Employee = None):
    """Restored an archived employee"""
    employee.is_archived = False
    employee.archived_at = None
    employee.archived_by = None
    employee.archived_reason = None
    employee.employment_status = 'Active'
    employee.save()
    messages.success(request, f'Employee {employee.employee_id} restored successfully')
    return JsonResponse({'success': True}, status=200)

# Delete employee
@login_required
@delegate_required
def delete_employee(request, emp_id: str, employee: Employee = None):
    """deletes an employee from the organizations branch. Raises error if no employee with the given id is found"""
    # ensure there's no transfer request pending for this employee. Settle or cancel it first
    if Transfer.objects.filter(employee=employee, status='Pending').exists():
        messages.error(request, 'A pending transfer exists for this employee. Settle or cancel it to proceed')
        return JsonResponse({'success': False}, status=200)
    employee.delete()
    messages.success(request, "Employee deleted successfully")
    return JsonResponse({'success': True}, status=200)




"""Leave Management"""
# Leave request
@require_POST
@login_required
def leave_request(request):
    """Employee leave request"""
    data = request.POST.dict()
    try:
        branch = Branch.objects.get(branch_id=data['branch_id'])
        employee = Employee.objects.filter(employee_id=data['employee_id'].strip(), branch=branch).first()
        if employee.branch.organization != request.user.branch.organization:
            raise PermissionDenied('You are not allowed to perform this operation')
        if request.user.is_delegate and request.user.branch != employee.branch:
            raise PermissionDenied('You are not allowed to perform this operation')

    except Employee.DoesNotExist:
        messages.error(request, "Employee not found")
        return redirect('branch_dashboard', branch_id=branch.branch_id)
    leave = Leave(employee=employee, leave_type=data['leave_type'], leave_start_date=parse_date(data['start_date']),
                   leave_end_date=parse_date(data['end_date']), leave_reason=data['reason'])
    leave.save()
    messages.success(request, f"Leave request submitted successfully")
    return redirect('branch_dashboard', branch_id=branch.branch_id)


# Accept and decline leave request
@csrf_exempt
@require_POST
@login_required
def manage_leave_request(request, leave_id):
    """Accept or decline leave request"""
    leave = get_object_or_404(Leave, pk=leave_id)
    if leave.employee.branch.organization != request.user.branch.organization:
        raise PermissionDenied('You are not allowed to perform this operation')

    action = request.POST.get('action')
    if action == 'accept':
        leave.leave_status = 'Approved'
        leave.save()
        messages.success(request, 'Leave request accepted')
    elif action == 'decline':
        leave.leave_status = 'Declined'
        leave.save()
        messages.success(request, 'Leave request declined')
    return JsonResponse({'success': True}, status=200)




"""Payroll Management"""
@login_required
@require_POST
def create_payroll(request):
    """Create payroll for an employee"""
    data = request.POST.dict()
    employee = get_object_or_404(Employee, employee_id=data['employee_id'], branch__branch_id=request.user.branch.branch_id)
    if employee.branch.organization != request.user.branch.organization:
        raise PermissionDenied('You are not allowed to perform this operation')

    employee.basic_salary = int(data['basic_salary'])
    employee.save()
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
                        performance_penalty=int(data['performance_penalty']), basic_salary=int(data['basic_salary'])
                      )
    payroll.save()
    messages.success(request, f"Payroll created successfully")
    return redirect('payroll_detail', payroll_id=payroll.id)


@login_required
def update_payroll(request, payroll_id):
    """Update payroll"""
    payroll = get_object_or_404(Payroll, id=payroll_id)
    if payroll.employee.branch.organization != request.user.branch.organization:
        raise PermissionDenied('You are not allowed to perform this operation')

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
        form = PayrollForm(instance=payroll, data=request.POST or None)
    return render(request, 'payroll/update_payroll.html', {'form': form})


@login_required
def payroll_detail(request, payroll_id):
    """Payroll detail"""
    payroll = get_object_or_404(Payroll, id=payroll_id)
    if payroll.employee.branch.organization != request.user.branch.organization:
        raise PermissionDenied('You are not allowed to perform this operation')

    if payroll.employee.branch.pk == request.user.branch.pk or payroll.employee.branch.organization.admin_user == request.user:
        return render(request, 'payroll/payroll_detail.html', {'payroll': payroll})
    raise PermissionDenied()

@login_required
@delegate_required
def payroll_history(request, emp_id: str, employee: Employee = None):
    """Returns payment history of the employee that matches the emp_id"""
    payroll_history = Payroll.objects.filter(employee=employee).order_by('-year', '-month')
    
    context = {
        'employee': employee,
        'payroll_history': payroll_history
    }
    return render(request, 'payroll/payroll_history.html', context)

@login_required
def delete_payroll(request, payroll_id):
    """Delete payroll"""
    payroll = get_object_or_404(Payroll, id=payroll_id)
    if request.user.is_delegate and request.user.branch != payroll.employee.branch:
        raise PermissionDenied('You are not allowed to perform this operation')
    if payroll.employee.branch.organization != request.user.branch.organization:
        raise PermissionDenied('You are not allowed to perform this operation')
    payroll.delete()
    messages.success(request, f'Payroll deleted successfully')
    return redirect('branch_dashboard', branch_id=payroll.employee.branch.branch_id)


"""Payroll Management"""
@login_required
@require_POST
def create_payroll_upload(request):
    """Create payroll for an employee"""
    data = request.POST.dict()
    employee = get_object_or_404(Employee, employee_id=data['employee_id'], branch__branch_id=request.user.branch.branch_id)
    if employee.branch.organization != request.user.branch.organization:
        raise PermissionDenied('You are not allowed to perform this operation')

    employee.basic_salary = int(data['basic_salary'])
    employee.save()
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
                        performance_penalty=int(data['performance_penalty']), basic_salary=int(data['basic_salary'])
                      )
    payroll.save()
    messages.success(request, f"Payroll created successfully")
    return redirect('payroll_detail', payroll_id=payroll.id)



"""Performance Management"""
# performance dashboard
@login_required
@delegate_required
def performance_dashboard(request, emp_id: str, employee: Employee = None):
    """Performance Dashboard"""    
    update_review_form, performance_id = None, None
    try:
        performance_instance = Performance.objects.filter(employee=employee).first()
        if performance_instance:
            update_review_form = PerformanceReviewForm(instance=performance_instance, data=request.POST or None)
            performance_id = performance_instance.id
        review_form = PerformanceReviewForm(data=request.POST or None)
    except Performance.DoesNotExist:
        pass

    performance = Performance.objects.filter(employee=employee)
    education = Education.objects.filter(employee=employee)
    work_history = WorkHistory.objects.filter(employee=employee)
    employee_docs = EmployeeDocs.objects.filter(employee=employee)
    payroll = Payroll.objects.filter(employee=employee)
    appointments = Appointments.objects.filter(employee=employee)
    attendance = Attendance.objects.filter(employee=employee)
    leave = Leave.objects.filter(employee=employee)
    return render(request, 'performance/performance_dashboard.html', 
                  {'employee': employee, 'performance': performance,
                    'education': education, 'work_history': work_history,
                    'employee_docs': employee_docs, 'performance_id': performance_id,
                    'payroll': payroll, 'appointments': appointments,
                    'attendance': attendance, 'leave': leave,
                    'review_form': review_form, 'update_review_form': update_review_form}
                    )


@login_required
@require_POST
@delegate_required
def performance_review(request, emp_id: str, employee: Employee = None):
    """Submit performance review"""
    form = PerformanceReviewForm(request.POST)
    if form.is_valid():
        performance = form.save(commit=False)
        performance.employee = employee
        performance.save()
        messages.success(request, 'Performance review submitted successfully')
    return redirect('performance_dashboard', emp_id=employee.employee_id)


# update project performance
@login_required
@require_POST
def update_performance_review(request, performance_id):
    """Update project performance"""
    performance = get_object_or_404(Performance, pk=performance_id)
    if request.user.is_delegate and request.user.branch != performance.employee.branch:
        raise PermissionDenied('You are not allowed to perform this operation')
    if performance.employee.branch.organization == request.user.branch.organization:
        form = PerformanceReviewForm(request.POST, instance=performance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project performance feedback updated successfully')
            return render(request, 'performance_dashboard.html', {'review_form': form})
    raise PermissionDenied('You are not allowed to perform this operation')



# delete performance review
@login_required
@csrf_exempt
def delete_performance_review(request, performance_id):
    """Delete performance review"""
    performance = get_object_or_404(Performance, pk=performance_id)
    if request.user.is_delegate and request.user.branch != performance.employee.branch:
        raise PermissionDenied('You are not allowed to perform this operation')
    if performance.employee.branch.organization == request.user.branch.organization:
        performance.delete()
        messages.success(request, 'Performance review deleted successfully')
        return redirect('branch_dashboard', branch_id=performance.employee.branch.branch_id)
    raise PermissionDenied('You are not allowed to perform this operation')




"""Transfer Management"""
@login_required
@require_POST
def transfer_request(request):
    """Submit transfer request"""
    org = get_object_or_404(Organization, id=request.user.branch.organization.id)
    form = TransferForm(org, request.user, request.POST)
    if form.is_valid():
        # check whether there is a pending transfer for this employee
        transfer_request = form.save(commit=False)
        if Transfer.objects.filter(employee=transfer_request.employee, status='Pending').exists():
            messages.error(request, 'This employee already has a pending transfer request')
            return redirect('branch_dashboard', branch_id=request.user.branch.branch_id)
        
        transfer_request.requested_by = request.user
        transfer_request.source_branch=request.user.branch
        transfer_request.organization = org
        transfer_request.save()
        messages.success(request, 'Transfer request submitted successfully.')
        return redirect('branch_dashboard', branch_id=request.user.branch.branch_id)
    else:
        messages.error(request, 'Failed to submit transfer request. Please check the form.')
        return redirect('branch_dashboard', branch_id=request.user.branch.branch_id)


# cancel transfer request
@login_required
@require_POST
def cancel_transfer_request(request, transfer_id):
    """Cancel transfer request"""
    transfer = get_object_or_404(Transfer, pk=transfer_id)
    if transfer.transfer_status == 'Pending':
        transfer.delete()
        messages.success(request, 'Transfer request cancelled successfully')
    else:
        messages.error(request, 'Transfer request cannot be cancelled')
    return redirect('branch_dashboard', branch_id=request.user.branch.branch_id)



# accept or decline transfer request
@login_required
@require_POST
@csrf_exempt
def manage_transfer_request(request, transfer_id):
    """Accept or decline transfer request"""
    if request.user.is_delegate:
        messages.error(request, 'You do not have permission to access this page')
        return redirect('branch_dashboard', branch_id=request.user.branch.branch_id)
    
    # org = request.user.branch.organization
    transfer = get_object_or_404(Transfer, pk=transfer_id)
    action = request.POST.get('action')
    if action == 'accept':
        transfer.status = 'Approved'
        transfer.employee.branch = transfer.destination_branch
        transfer.employee.save()
        transfer.save()
        messages.success(request, 'Transfer request accepted')
    elif action == 'decline':
        transfer.status = 'Declined'
        transfer.save()
        messages.success(request, 'Transfer request declined')
    return JsonResponse({'success': True}, status=200)





"""Reports Management and Statistics"""
# create a report
@login_required
def create_report(request, branch_id=None):
    """Create a report"""
    branch = get_object_or_404(Branch, branch_id=branch_id)    
    try:
        report = Report.objects.filter(branch=branch).first()
        if report:
            report_id = report.id
            update_form = ReportForm(instance=report, initial={'created_by': request.user, 'branch': branch}, data=request.POST or None, files=request.FILES or None)
        else:
            report_id = None
            update_form = ReportForm(initial={'created_by': request.user, 'branch': branch}, data=request.POST or None, files=request.FILES or None)
        form = ReportForm(initial={'created_by': request.user, 'branch': branch}, data=request.POST or None, files=request.FILES or None)

    except Report.DoesNotExist:
        pass

    reports = Report.objects.filter(branch=branch)
    
    user = request.user
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report_instance = form.save(commit=False)
            report_instance.branch = branch
            report_instance.created_by = user
            report_instance.save()
            messages.success(request, 'Report created successfully')
            return redirect('create_report', branch_id=branch.branch_id)
        else:
            messages.error(request, 'Failed to create report. Please check the form.')
            return redirect('create_report')
    return render(request, 'reports/reports.html', {'form': form, 'user': user, 'report_id': report_id, 'reports': reports,
                                                    'update_form': update_form, 'branch_id': branch_id})


# Update a report
@login_required
@require_POST
def update_report(request, report_id):
    """Update a report"""
    report = get_object_or_404(Report, pk=report_id)
    form = ReportForm(request.POST, instance=report)
    if form.is_valid():
        form.save(commit=False)
        form.instance.version += 1
        form.save()
        messages.success(request, 'Report updated successfully')
        return redirect('branch_dashboard', branch_id=request.user.branch.branch_id)
    else:
        messages.error(request, 'Failed to update report. Please check the form.')
        return redirect('branch_dashboard', branch_id=request.user.branch.branch_id)

# Org statistics
@login_required
def statistics(request):
    """ Render organization statistics"""
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access this page')
        return redirect('branch_dashboard', branch_id=request.user.branch.branch_id)
    
    organization = Organization.objects.filter(id=request.user.branch.organization.id).first()
    fin_reports = Finance.objects.filter(branch__organization=organization)


        # Overall Statistics
    employees = Employee.objects.filter(branch__organization=organization)
    branches = Branch.objects.filter(organization=organization)
    total_branches_count = branches.count()

        # Finance statistics
    total_employee_salary = sum([p.net_pay for p in  Payroll.objects.filter(employee__branch__organization=organization)])
    total_employees = employees.count()
    total_revenue = sum([r.total_revenue for r in fin_reports])
    total_expenses = sum([r.total_expenses for r in fin_reports])
    total_profit = total_revenue - total_expenses
    total_reports = fin_reports.count()

   # employee statistics
    
    total_employees_count = employees.count()
    archived_employees_count = employees.filter(is_archived=True).count()
    active_employees_count = employees.filter(is_archived=False, employment_status='Active').count()
    inactive_employees_count = employees.exclude(employment_status='Active').count()
    total_employees_on_leave_count = Leave.objects.filter(employee__branch__organization=organization, 
                                                          leave_status='Approved', leave_end_date__gte=timezone.now().date()).count()
    monthly_created_employees = sum([b.monthly_created_employees for b in branches])

    # leave statistics
    leave_requests = Leave.objects.filter(employee__branch__organization=organization)
    pending_leave_requests = leave_requests.filter(leave_status='Pending').count()
    approved_leave_requests = leave_requests.filter(leave_status='Approved').count()
    declined_leave_requests = leave_requests.filter(leave_status='Declined').count()
    active_leave = leave_requests.filter(leave_status='Approved', leave_end_date__gte=timezone.now().date())
    leave_history = leave_requests.filter(leave_status='Approved', leave_end_date__lt=timezone.now()) # used for average leave duration
    leave_durations = [(leave.leave_end_date - leave.leave_start_date).days for leave in leave_history]
    average_leave_duration = mean(leave_durations) if leave_durations else 0

    # payroll statistics
    payroll = Payroll.objects.filter(employee__branch__organization=organization).order_by('-year', '-month')
    total_payroll = payroll.count()
    total_netpay = sum([p.net_pay for p in payroll])
    total_deductions = sum([p.total_deductions for p in payroll])
    total_allowances = sum([p.total_allowance for p in payroll])
    average_netpay = total_netpay / total_payroll if total_payroll else 0
    total_payment = total_netpay + total_allowances

    # performance statistics
    performance = Performance.objects.filter(employee__branch__organization=organization).order_by('-performance_rating')
    underperforming_employees = performance.filter(performance_rating__lt=60)
    average_performance_rating = mean([p.performance_rating for p in performance]) if performance else 0
    high_performers = performance.filter(performance_rating__gte=80)
    improvement_rate = (high_performers.count() / performance.count()) * 100 if performance else 0
    highest_rating = performance.first()
    employee_engagement = 'High' if average_performance_rating >= 70 else 'Low'

    """Transfer Statistics"""
    transfers = Transfer.objects.filter(organization=organization)
    pending_transfers = transfers.filter(status='Pending')
    approved_transfers = transfers.filter(status='Approved')
    declined_transfers = transfers.filter(status='Declined')
    monthly_transfer_count = transfers.filter(created_at__month=timezone.now().month).count()
    last_month_transfer_count = transfers.filter(created_at__month=timezone.now().month-1).count()
    employees = Employee.objects.filter(branch__organization=organization)




    """context"""
    context = {'org': organization, 'branches': branches, 'transfers': transfers, 'pending_transfers': pending_transfers,
                'approved_transfers': approved_transfers, 'declined_transfers': declined_transfers, 'monthly_transfer_count': monthly_transfer_count,
                'last_month_transfer_count': last_month_transfer_count, 'employees': employees, 'total_branches_count': total_branches_count,
                'total_employees_count': total_employees_count, 'archived_employees_count': archived_employees_count, 'active_employees_count': active_employees_count,
                'inactive_employees_count': inactive_employees_count, 'active_leave': active_leave, 'total_employees_on_leave_count': total_employees_on_leave_count,
                'monthly_created_employees': monthly_created_employees, 'pending_leave_requests': pending_leave_requests, 'approved_leave_requests': approved_leave_requests,
                'declined_leave_requests': declined_leave_requests, 'average_leave_duration': average_leave_duration, 'payroll': payroll, 'total_payroll': total_payroll,
                'total_payment': total_payment, 'total_deductions': total_deductions, 'total_allowances': total_allowances, 'total_netpay': total_netpay,
                'average_salary': average_netpay, 'performance': performance, 'underperformance': underperforming_employees, 'average_performance_rating': average_performance_rating,
                'high_performers': high_performers, 'improvement_rate': improvement_rate, 'highest_rating': highest_rating, 'employee_engagement': employee_engagement,
                'leave_requests': leave_requests, 'leave_history': leave_history, 'total_employee_salary': total_employee_salary, 'total_employees': total_employees,
                'total_revenue': total_revenue, 'total_expenses': total_expenses, 'total_profit': total_profit, 'total_reports': total_reports
                }



    return render(request, 'reports/statistics.html', context=context)



"""Finance Management"""
@login_required
def finance_report(request, type=None, branch_id=None):
    """Create a finance report"""
    branch = get_object_or_404(Branch, branch_id=branch_id)
    
    basic_form = BasicFinanceForm(initial={'created_by': request.user, 'branch': branch}, data=request.POST or None, files=request.FILES or None)
    detailed_form = DetailedFinanceForm(initial={'created_by': request.user, 'branch': branch}, data=request.POST or None, files=request.FILES or None)
    reports = Finance.objects.filter(branch=branch)
    user = request.user

    # Finance statistics
    total_employee_salary = sum([p.net_pay for p in Payroll.objects.filter(employee__branch=branch)])
    total_employees = Employee.objects.filter(branch=branch).count()
    total_revenue = sum([r.total_revenue for r in reports])
    total_expenses = sum([r.total_expenses for r in reports])
    total_profit = total_revenue - total_expenses
    total_reports = reports.count()

    context =  {'basic_form': basic_form, 'user': user, 'reports': reports, 'branch_id': branch_id, 'type': type,
                'detailed_form': detailed_form, 'branch': branch, 'total_employee_salary': total_employee_salary,
                'total_employees': total_employees, 'total_revenue': total_revenue, 'total_expenses': total_expenses,
                'total_profit': total_profit, 'total_reports': total_reports
                }
    if request.method == 'POST':
        if type == 'basic':
            form = BasicFinanceForm(request.POST, request.FILES)
        else:
            form = DetailedFinanceForm(request.POST, request.FILES)
            
        if form.is_valid():
            report_instance = form.save(commit=False)
            report_instance.branch = branch
            report_instance.created_by = user
            report_instance.save()
            messages.success(request, 'Finance report created successfully')
            return redirect('finance_dashboard', branch_id=branch.branch_id)
        else:
            messages.error(request, 'Failed to create finance report. Please check the form.')
            return redirect('finance_dashboard', branch_id=branch.branch_id)
    return render(request, 'reports/finances.html', context=context)




"""Account Settings"""
@login_required
@require_POST
def profile_settings(request):
    form = UserProfileForm(request.POST, request.FILES, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Profile settings updated successfully')
        return redirect('branch_dashboard', branch_id=request.user.branch.branch_id)
    else:
        messages.error(request, 'Failed to update profile settings. Please check the form.')
        return redirect('branch_dashboard', branch_id=request.user.branch.branch_id)


@login_required
@require_POST
def change_password(request):
    if request.user.can_change_password:
        form = ChangePasswordForm(request.user, request.POST or None)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password changed successfully')
            return redirect('branch_dashboard', branch_id=request.user.branch.branch_id)
        else:
            messages.error(request, 'Failed to change password. Please check the form.')
            return redirect('branch_dashboard', branch_id=request.user.branch.branch_id)
    else:
        messages.error(request, 'You do not have permission to change password')
        return redirect('branch_dashboard', branch_id=request.user.branch.branch_id)


@login_required
@require_POST
def upload_documents(request):
    organization = request.user.branch.organization
    form = BranchDocumentsForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.organization = organization
        instance.save()
        messages.success(request, 'Document uploaded successfully')
        return redirect('branch_dashboard', branch_id=request.user.branch.branch_id)
    else:
        messages.error(request, 'Failed to upload document. Please check the form.')
        return redirect('branch_dashboard', branch_id=request.user.branch.branch_id)


@login_required
@require_POST
def reset_delegate_password(request):
    """Reset delegate password"""
    if request.user.can_change_password:
        delegate = get_object_or_404(AdminUser, id=request.POST.get('delegate_id').strip())
        if not delegate or not delegate.is_delegate or not delegate.branch.organization == request.user.branch.organization:
            messages.error(request, 'Invalid delegate')
            return redirect('branch_dashboard', branch_id=request.user.branch.branch_id)
        new_password = request.POST.get('password').strip()
        can_change_password = request.POST.get('can_change_password').strip()
        delegate.set_password(new_password)
        delegate.can_change_password = True if int(can_change_password) else False
        delegate.save()
        messages.success(request, 'Password reset successfully')
        return JsonResponse({'success': True}, status=200)
    else:
        messages.error(request, 'You do not have permission to reset password')
        return redirect('branch_dashboard', branch_id=request.user.branch.branch_id)





# promote delegate to superuser
@login_required
@csrf_exempt
@require_POST
def promote_delegate(request, delegate_id):
    """Promote delegate to superuser"""
    if request.user.is_superuser:
        delegate = get_object_or_404(AdminUser, id=delegate_id)
        if not delegate or not delegate.is_delegate or not delegate.branch.organization == request.user.branch.organization:
            messages.error(request, 'You cannot promote this delegate to superuser')
            return JsonResponse({'success': False}, status=200)
        delegate.is_superuser = True
        delegate.is_delegate = False
        delegate.can_change_password = True
        delegate.save()
        messages.success(request, 'Delegate promoted to superuser successfully')
        return JsonResponse({'success': True}, status=200)
    else:
        messages.error(request, 'You do not have permission to promote delegate')
        return JsonResponse({'success': False}, status=200)


# demote superuser to delegate
@login_required
@csrf_exempt
@require_POST
def demote_admin(request, admin_id):
    """Demote superuser to delegate"""
    if request.user.is_superuser:
        delegate = get_object_or_404(AdminUser, id=admin_id)
        if not delegate.is_superuser or not delegate.branch.organization == request.user.branch.organization\
            or delegate == request.user or delegate.branch.organization.admin_user == delegate:
            messages.error(request, 'You cannot demote this superuser to delegate')
            return JsonResponse({'success': False}, status=200)
        delegate.is_superuser = False
        delegate.is_delegate = True
        delegate.can_change_password = False
        delegate.save()
        messages.success(request, 'Superuser demoted to delegate successfully')
        return JsonResponse({'success': True}, status=200)
    else:
        messages.error(request, 'You do not have permission to demote superuser')
        return JsonResponse({'success': False}, status=200)


#  suspend admin user
@login_required
@csrf_exempt
@require_POST
def suspend_admin(request, admin_id):
    """Suspend admin user"""
    if request.user.is_superuser:
        admin = get_object_or_404(AdminUser, id=admin_id)
        if not admin or admin == request.user or admin.branch.organization.admin_user == admin:
            messages.error(request, 'You cannot suspend this user')
            return JsonResponse({'success': False}, status=200)
        admin.is_active = False
        admin.employment_status = 'Suspended'
        admin.can_change_password = False
        admin.save()
        messages.success(request, 'User suspended successfully')
        return JsonResponse({'success': True}, status=200)
    else:
        messages.error(request, 'You do not have permission to suspend user')
        return JsonResponse({'success': False}, status=200)


# restore suspended admin
@login_required
@csrf_exempt
@require_POST
def restore_admin(request, admin_id):
    """Restore suspended admin user"""
    if request.user.is_superuser:
        admin = get_object_or_404(AdminUser, id=admin_id)
        if not admin or admin == request.user or admin.branch.organization.admin_user == admin:
            messages.error(request, 'You cannot restore this user')
            return JsonResponse({'success': False}, status=200)
        admin.is_active = True
        admin.employment_status = 'Active'
        admin.can_change_password = True
        admin.is_superuser = True
        admin.save()
        messages.success(request, 'User restored successfully')
        return JsonResponse({'success': True}, status=200)
    else:
        messages.error(request, 'You do not have permission to restore user')
        return JsonResponse({'success': False}, status=200)



"""Search Feature"""
@login_required
def search_employee(request):
    if request.method == 'GET':
        search_term = request.GET.get('search_term', '')
        if search_term:
            # Perform the search query across multiple fields
            employees = Employee.objects.filter(
                Q(first_name__icontains=search_term) |
                Q(last_name__icontains=search_term) |
                Q(middle_name__icontains=search_term) |
                Q(employee_id__icontains=search_term) |
                Q(email__icontains=search_term)
            )
        else:
            # Return all employees if no search term provided
            employees = Employee.objects.none()
        return render(request, 'search_results.html', {'employees': employees})


# Forgot Password
def forgot_password(request):
    """Forgot Password"""
    if request.method == 'POST':
        recipient = request.POST.get('email').strip()
        token = generate_password_reset_token()
        try:
            user = AdminUser.objects.get(email=recipient)
        except AdminUser.DoesNotExist:
            messages.error(request, 'No admin user found with this email')
            return redirect('login')
        if not user.can_change_password:
            messages.error(request, 'You do not have permission to reset password, please contact your admin')
            return redirect('login')
        # Use get_or_create to create a new PasswordResetToken if it doesn't exist
        password_reset_token, created = PasswordResetToken.objects.get_or_create(user=user)
        password_reset_token.token = token
        password_reset_token.created_at = timezone.now()  # Update the created_at field
        password_reset_token.save()

        # Call the Celery task to send the password reset email asynchronously
        send_password_reset_email.delay(recipient, token)

        messages.success(request, 'Password reset code sent successfully')
        return render(request, 'password/reset_token.html', context={'user_email': recipient})
    return render(request, 'employee/login.html', context={'user_email': recipient})

# Genereate password reset token
def generate_password_reset_token():
    """Generate password reset token"""
    while True:
        first_digit = random.choice(string.digits[1:])
        rest_of_digits = ''.join(random.choices(string.digits, k=5))
        token = first_digit + rest_of_digits
        if not PasswordResetToken.objects.filter(token=token).exists():
            return int(token)


#confirm password reset token
def confirm_password_reset_token(request, email):
    """Confirm password reset token"""
    if request.method == 'POST':
        token = request.POST.get('token')
        user_email = email.strip()
        user = get_object_or_404(AdminUser, email=user_email)
        
        try:
            password_reset_token = PasswordResetToken.objects.get(user=user)
        except PasswordResetToken.DoesNotExist:
            messages.error(request, 'User does not exist')
            return render(request, 'password/reset_token.html', context={'user_email': email})
        # Check if the provided token matches and is not expired
        if token == password_reset_token.token and not password_reset_token.is_expired():
            # Token is valid, you can proceed with the next steps
            messages.success(request, 'Token is valid, you can reset your password')
            return render(request, 'password/reset_password.html', context={'user_email': user_email, 'token': token})
        else:
            messages.error(request, 'Invalid or expired token')
            return redirect('login')
    return render(request, 'password/reset_token.html', context={'user_email': email})


# reset password
def reset_password(request, email):
    """Reset Password"""
    if request.method == 'POST':
        password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmPassword')
        token = request.POST.get('token')
        email = email.strip()
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'password/reset_password.html', context={'user_email': email, 'token': token})
        try:
            user = get_object_or_404(AdminUser, email=email)
            if user.password_reset_token.token == token and not user.password_reset_token.is_expired():
                user.set_password(password)
                user.save()
                messages.success(request, 'Password reset successful, Please Login')
                return redirect('login')
        except AdminUser.DoesNotExist:
            messages.error(request, 'User does not exist')
            return redirect('login')
    return render(request, 'employees/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You Logged Out")
    return redirect('login') 


# Error 404
def error_404(request, exception):
    return render(request, 'error/404.html', status=404) # Renders error 404 page from project templates

# Error 500
def error_500(request):
    return render(request, 'error/500.html', status=500)

# Error 403
def error_403(request, exception):
    return render(request, '403.html', status=403)# Renders error 403 page




""" Footer Section Navs"""
def quick_guide(request):
    """Guide for getting started"""
    return render(request, 'navs/quick_guide.html')

def privacy(request):
    """Privacy Policy"""
    return render(request, 'navs/privacy.html')

def terms(request):
    """Terms and Conditions"""
    return render(request, 'navs/terms.html')

def about(request):
    """About Us"""
    return render(request, 'navs/about.html')

def faq(request):
    return render(request, 'navs/faq.html')

def developers(request):
    """Developers"""
    return render(request, 'navs/developers.html')

# favicon
def favicon(request):
    """Favicon logo"""
    return redirect('/static/base/images/logo.png')



###############################################################
# File Processing for multiple operations -> CSV, Excel
###############################################################

""" Employee creation from csv or excel file"""
@login_required
@require_POST
@login_required
@require_POST
def upload_employee_data(request, branch_id: str):
    """Uploads employee data from Excel or CSV file."""
    branch = get_object_or_404(Branch, branch_id=branch_id)
    if branch.organization != request.user.branch.organization:
        raise PermissionDenied('You are not allowed to perform this operation')
    if request.user.is_delegate and request.user.branch != branch:
        raise PermissionDenied('You are not allowed to perform this operation')

    form = EmployeesUploadForm(request.POST, request.FILES)
    if form.is_valid():
        # Get file content and filename
        file_content = request.FILES['file'].read()
        filename = request.FILES['file'].name

        user_id = request.user.id
        print(filename, filename.lower())
        # Call the Celery task to process the uploaded file
        result = process_employee_data.delay(file_content=file_content, filename=filename, branch_id=branch_id, user_id=user_id)

        # Check if the task was successful
        try:
            task_result = result.get()
            if task_result['success']:
                messages.success(request, task_result['message'])
            else:
                messages.error(request, task_result['message'])
        except Exception as e:
            # Handle exception if task retrieval fails
            messages.error(request, f'Error processing task: {e}')

        return redirect('branch_dashboard', branch_id=branch.branch_id)
    # return last error message if form is not valid
    last_error = form.errors[list(form.errors.keys())[-1]][-1]
    messages.error(request, f'Error occurred: {last_error}')
    return redirect('branch_dashboard', branch_id=branch.branch_id)


"""Payroll Management"""
@login_required
@require_POST
def create_payroll_upload(request, branch_id: str):
    """Create payroll for an employee"""
    branch = get_object_or_404(Branch, branch_id=branch_id)
    if branch.organization != request.user.branch.organization:
        raise PermissionDenied('You are not allowed to perform this operation')
    if request.user.is_delegate and request.user.branch != branch:
        raise PermissionDenied('You are not allowed to perform this operation')
    
    form = PayrollUploadForm(request.POST, request.FILES)
    if form.is_valid():
        # Get file content and filename
        file_content = request.FILES['file'].read()
        filename = request.FILES['file'].name

        # Call the Celery task to process the uploaded file
        result = process_payroll_data.delay(file_content=file_content, filename=filename, branch_id=branch_id)

        # Check if the task was successful
        try:
            task_result = result.get()
            if task_result['success']:
                messages.success(request, task_result['message'])
            else:
                messages.error(request, task_result['message'])
        except Exception as e:
            # Handle exception if task retrieval fails
            messages.error(request, f'Error processing task: {e}')

        return redirect('branch_dashboard', branch_id=branch.branch_id)
    
    # If form is not valid, redirect back to branch dashboard with error message
    last_error = form.errors[list(form.errors.keys())[-1]][-1]
    messages.error(request, f'Error occurred: {last_error}')
    return redirect('branch_dashboard', branch_id=branch.branch_id)
