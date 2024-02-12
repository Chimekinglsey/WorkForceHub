from turtle import back
from django.shortcuts import render, redirect
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .backends import AdminUserAuthBackend
from django.contrib.auth import login, logout
from employees.models import Employee, AdminUser, PasswordResetToken, Education, WorkHistory,\
      Performance, BankDetails, EmployeeDocs, Payroll, Appointments, Attendance, Leave
from organizations.models import Organization, Branch
from .forms import SignUpForm, ProfileUpdateForm, BranchForm
from django.http import JsonResponse, Http404
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
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
        print('username_or_email:', username_or_email, 'password:', password)

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
        form = ProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            # Replace old profile picture with new one
            if 'profile_picture' in form.cleaned_data:
                if request.user.profile_picture:
                    request.user.profile_picture.delete()
            form.instance.employee_id = request.user.employee_id  # Set employee_id from logged-in user
            form.save()
            # Redirect to a success page or any other desired view

            messages.success(request, 'Profile updated successfully')
            return redirect('create_org')
    else:
        # Initialize form with employee_id from logged-in user
        form = ProfileUpdateForm(initial={'employee_id': request.user.employee_id})
    return render(request, 'employees/profile_update.html', {'form': form})# AdminUser Logout   


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
        # Remove csrfmiddlewaretoken key from the dictionary
        org_data.pop('csrfmiddlewaretoken', None)
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