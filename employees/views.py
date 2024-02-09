from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from employees.models import Employee, AdminUser, PasswordResetToken, Education, WorkHistory,\
      Performance, BankDetails, EmployeeDocs, Payroll, Appointments, Attendance, Leave
from .forms import SignUpForm
from django.contrib.auth import logout
from django.http import JsonResponse
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.urls import reverse
import random, string



# landing page
def landing_page(request):
    """WorkForceHub HOMEPAGE"""
    return render(request, 'employees/landing_page.html')

# signup page
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'employees/signup.html', {'form': form})

# login page
def login(request):
    """Login page"""
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST['password']
        if '@' in username:
           user = authenticate(request, email=username, password=password)
        else:
            user = authenticate(request, username=username, password=password)
        if user:
            messages.success(request, 'Login successful')
            return redirect('landing_page')
        else:
            context = {
                'username': username,
                'password': password
            }
            messages.error(request, 'Invalid username or password')
            return render(request, 'employees/login.html', context)
    return render(request, 'employees/login.html')



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

            message = f"Your password reset code is {token} (expires in one hour).\n\nPlease do not share this code with anyone\nIf you didn't request this pin, we recommend you change your WorkForceHub password.\n\nRegards,\Kingsley, WorkForceHub Team"
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


# AdminUser Logout   
def logout(request):
    logout(request)
    messages.success(request, "You're Logged Out")
    return redirect('login') 