from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group, Permission
from datetime import datetime, date
from django.utils import timezone
from organizations.models import Branch
from PIL import Image
from django.core.files.storage import default_storage
from statistics import mean


# choices
GENDER_CHOICES = (
    ('--Select--', _('--Select--')),
    ('Male', _('Male')),
    ('Female', _('Female')),
)

MARITAL_STATUS_CHOICES = (
    ('--Select--', _('--Select--')),
    ('Single', _('Single')),
    ('Married', _('Married')),
    ('Divorced', _('Divorced')),
    ('Widowed', _('Widowed')),
    ('Separated', _('Separated')),
    ('Other', _('Other'))
)

EMPLOYMENT_STATUS_CHOICES = (
    ('--Select--', _('--Select--')),
    ('Active', _('Active')),
    ('Inactive', _('Inactive')),
    ('Suspended', _('Suspended')),
    ('Terminated', _('Terminated')),
    ('Resigned', _('Resigned')),
    ('Retired', _('Retired')),
    ('Deceased', _('Deceased')),
    ('On Leave', _('On Leave')),
    ('On Training', _('On Training')),
    ('On Probation', _('On Probation')),        
    ('Other', _('Other'))
)

EMPLOYMENT_TYPE_CHOICES = (
    ('--Select--', _('--Select--')),
    ('Remote', _('Remote')),
    ('Hybrid', _('Hybrid')),
    ('On-site', _('On-site')),
    ('Other', _('Other'))
)

EMPLOYEE_STATUS_CHOICES = (
    ('--Select--', _('--Select--')),
    ('Full-time', _('Full-time')),
    ('Part-time', _('Part-time')),
    ('Contract', _('Contract')),
    ('Intern', _('Intern')),
    ('Volunteer', _('Volunteer')),
    ('Temporary', _('Temporary')),
    ('Seasonal', _('Seasonal')),
    ('Freelance', _('Freelance')),
    ('Remote', _('Remote')),
    ('Disabled', _('Disabled')),
    ('Other', _('Other'))
)

LEVEL_CHOICES = (
    ('--Select--', _('--Select--')),
    ('Entry-level', _('Entry-level')),
    ('Mid-level', _('Mid-level')),
    ('Senior-level', _('Senior-level')),
    ('Executive', _('Executive')),
    ('Top-level', _('Top-level')),
    ('Other', _('Other'))
)

DESIGNATION_CHOICES = (
    ('--Select--', _('--Select--')),
    ('Employee', _('Employee')),
    ('Intern', _('Intern')),
    ('Trainee', _('Trainee')),
    ('Associate', _('Associate')),
    ('Assistant', _('Assistant')),
    ('Officer', _('Officer')),
    ('Analyst', _('Analyst')),
    ('Coordinator', _('Coordinator')),
    ('Specialist', _('Specialist')),
    ('Consultant', _('Consultant')),
    ('Advisor', _('Advisor')),
    ('Supervisor', _('Supervisor')),
    ('Manager', _('Manager')),
    ('Director', _('Director')),
    ('Executive', _('Executive')),
    ('President', _('President')),
    ('CEO', _('CEO')),
    ('CFO', _('CFO')),
    ('CTO', _('CTO')),
    ('CIO', _('CIO')),
    ('COO', _('COO')),
    ('Chairman', _('Chairman')),
    ('Board Member', _('Board Member')),
    ('Other', _('Other'))
)

NEXT_OF_KIN_RELATIONSHIP_CHOICES = (
    ('--Select--', _('--Select--')),
    ('Spouse', _('Spouse')),
    ('Child', _('Child')),
    ('Parent', _('Parent')),
    ('Sibling', _('Sibling')),
    ('Relative', _('Relative')),
    ('Friend', _('Friend')),
    ('Other', _('Other'))
)
# def resize_and_save_image(image_file, target_path, max_size=(300, 300), format='JPEG'):
#     """
#     Resize the given image file and save it to the specified target path in AWS S3.
#     """
#     try:
#         # Open the image
#         image = Image.open(image_file)

#         # Convert image to RGB mode if it's not already in RGB
#         if image.mode not in ('RGB', 'L'):
#             image = image.convert('RGB')

#         if image.height > max_size[1] or image.width > max_size[0]:
#             image.thumbnail(max_size)

#         # Save the resized image to S3 using default_storage
#         with default_storage.open(target_path, "wb") as fh:
#             image.save(fh, format=format)

#         return True  # Operation successful
#     except Exception as e:
#         # Log the error or handle it as needed
#         print(f"Error resizing and saving image: {e}")
#         return False  # Operation failed


def resize_and_save_image(image_file, target_path, max_size=(300, 300), format='JPEG'):
  """
  Resize the given image file and save it to the specified target path in AWS S3.
  Handles cases where no image is provided.
  """
  try:
    if not image_file:  # Check if image_file is empty or None
      return False  # No image to process

    # Open the image
    image = Image.open(image_file)

    # Convert image to RGB mode if it's not already in RGB
    if image.mode not in ('RGB', 'L'):
      image = image.convert('RGB')

    if image.height > max_size[1] or image.width > max_size[0]:
      image.thumbnail(max_size)

    # Save the resized image to S3 using default_storage
    with default_storage.open(target_path, "wb") as fh:
      image.save(fh, format=format)

    return True  # Operation successful
  except Exception as e:
    # Log the error or handle it as needed
    print(f"Error resizing and saving image: {e}")
    return False  # Operation failed

class BaseUser(models.Model):
    """Base model containing common fields for AdminUser and Employee"""
    # Personal Information
    middle_name = models.CharField(_('Middle name'), max_length=30, null=True, blank=True)
    dob = models.DateField(_('Date of birth'), null=True, blank=True)
    gender = models.CharField(_('Gender'), max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    marital_status = models.CharField(_('Marital status'), choices=MARITAL_STATUS_CHOICES, max_length=15, null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True, blank=True)
    address = models.CharField(_('Address'), max_length=100, null=True, blank=True)
    nationality = models.CharField(_('Nationality'), max_length=30, null=True, blank=True)
    state_of_origin = models.CharField(_('State of origin'), max_length=30, null=True, blank=True)
    phone_number = models.CharField(_('Phone number'), max_length=15, null=True, blank=True)
    
    # Employment Information
    employee_id = models.CharField(_('Employee ID'), max_length=100, null=True, blank=True) # removed uniqe contraint to allow for multiple employees with same employee_id
    department = models.CharField(_('Department/division'), max_length=100)
    job_role = models.CharField(_('Job role'), max_length=100, null=True, blank=True)
    joining_date = models.DateField(_('Joining date'), null=True, blank=True)
    employment_type = models.CharField(_('Employment type'), choices=EMPLOYEE_STATUS_CHOICES, max_length=100)
    employment_status = models.CharField(_('Employment status'), choices=EMPLOYMENT_STATUS_CHOICES, max_length=20, default='Active')
    designation = models.CharField(_('Designation'), choices=DESIGNATION_CHOICES, max_length=30, default='Employee')
    level = models.CharField(_('Level'), choices=LEVEL_CHOICES, max_length=30, null=True, blank=True)
    last_promotion_date = models.DateField(_('Last promotion date'), null=True, blank=True)
    next_promotion_date = models.DateField(_('Next promotion date'), null=True, blank=True)
    basic_salary = models.PositiveIntegerField(_('Salary'), default=0, blank=True)
    
    # Bank Information
    bank_name = models.CharField(_('bank name'), max_length=30, null=True, blank=True)
    account_number = models.CharField(_('account number'), max_length=30, null=True, blank=True)
    account_name = models.CharField(_('account name'), max_length=100, null=True, blank=True)
    pension_id = models.CharField(_('pension ID'), max_length=30, null=True, blank=True)
    tax_id = models.CharField(_('tax ID'), max_length=30, null=True, blank=True)

    # Other Information
    emergency_contacts = models.TextField(_('Emergency contacts'), null=True)
    termination_resignation_date = models.DateField(_('Date of termination/resignation'), null=True, blank=True)
    highest_qualification = models.CharField(_('Highest qualification'), max_length=100, null=True, blank=True)
    highest_certificate = models.FileField(_('Highest certificate'), upload_to='employees/highest_certificates/', null=True, blank=True)
    employment_letter = models.FileField(_('Employment letter'), upload_to='employees/employment_letters/', null=True, blank=True)
    skills_qualifications = models.TextField(_('Skills/qualifications'), null=True, blank=True)
    is_archived = models.BooleanField(_('Archived status'), default=False)
    archived_at = models.DateTimeField(_('Archived at'), null=True, blank=True)
    archived_by = models.CharField(_('Archived by'), max_length=100, null=True, blank=True)
    archived_reason = models.TextField(_('Archived reason'), null=True, blank=True)

    # Next of kin
    next_of_kin_name = models.CharField(_('Next of kin name'), max_length=100, null=True, blank=True)
    next_of_kin_relationship = models.CharField(_('Next of kin relationship'), max_length=100, choices=NEXT_OF_KIN_RELATIONSHIP_CHOICES, null=True, blank=True)
    next_of_kin_phone_number = models.CharField(_('Next of kin phone number'), max_length=15, null=True, blank=True)
    # next_of_kin_address = models.CharField(_('Next of kin address'), max_length=100, null=True, blank=True)

    
    # Relationships
    supervised_employees = models.ManyToManyField('self', blank=True)

    # Timestamps
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    
    class Meta:
        abstract = True

class AdminUser(BaseUser, AbstractUser):
    """Custom User model for administrators"""
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True, related_name='admin_user')
    profile_picture = models.ImageField(_('Profile picture'), upload_to='adminuser/profile_pictures', default='default_picture.png', null=True, blank=True)
    adminuser = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='administrator')
    is_delegate = models.BooleanField(_('Delegate status'), default=False, help_text=_('Designates whether the user can act as a delegate for the organization.'))
    is_admin = models.BooleanField(_('Admin status'), default=True, help_text=_('Designates whether the user can log into this admin site.'))
    is_superuser = models.BooleanField(_('superuser status'), default=True, help_text=_('Designates that this user has all permissions without explicitly assigning them.'))
    can_change_password = models.BooleanField(_('Change password status'), default=True, help_text=_('Designates whether the user can change their password.'))
    delegated_branches = models.ManyToManyField(Branch, related_name='authorized_delegates')
    is_master_admin = models.BooleanField(_('Master admin status'), default=False, help_text=_('Designates whether the user is the master admin for the organization.'))
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='admin_user_permissions')
    groups = models.ManyToManyField(Group, blank=True, related_name='admin_user_groups')
    # TODO: Allow delegate admins to manage multiple branches
    

    
    class Meta:
        verbose_name = _('Administrator')
        verbose_name_plural = _('Admins')
        ordering = ['last_name', 'first_name']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the superclass save method
        target_path = "adminuser/profile_pictures/"
        if self.profile_picture:
            try:
                resize_and_save_image(self.profile_picture, target_path)
            except Exception as e:
                print(f"Error resizing and saving profile picture to S3: {e}")
                # Optional: Handle the error here, like logging or raising a specific exception

    def __str__(self):
        return self.username

class Employee(BaseUser):
    """Model for employees managed by users"""
    adminuser = models.ForeignKey(AdminUser, on_delete=models.CASCADE, related_name='managed_employees')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='employee')
    first_name = models.CharField(_('First name'), max_length=30)
    last_name = models.CharField(_('Last name'), max_length=30)
    profile_picture = models.ImageField(_('Profile picture'), upload_to='employees/profile_pictures', default='default_picture.png', null=True, blank=True)
    
    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        ordering = ['last_name', 'first_name']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the superclass save method
        target_path = "employees/profile_pictures/"
        if self.profile_picture:
            try:
                resize_and_save_image(self.profile_picture, target_path)
            except Exception as e:
                print(f"Error resizing and saving profile picture to S3: {e}")
                # Optional: Handle the error here, like logging or raising a specific exception
                
    def __str__(self):
        return f'{self.last_name} {self.first_name}'

class PasswordResetToken(models.Model):
    user = models.OneToOneField(AdminUser, on_delete=models.CASCADE, related_name='password_reset_token')
    token = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        # Check if the token has expired (e.g., one-hour expiry)
        return (timezone.now() - self.created_at).total_seconds() > 3600

class Appointments(models.Model):
    """Model for employee appointments"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField(_('appointment date'), null=True, blank=True)
    appointment_time = models.TimeField(_('appointment time'), null=True, blank=True)
    appointment_type = models.CharField(_('appointment type'), max_length=30, null=True, blank=True)
    appointment_reason = models.TextField(_('appointment reason'), null=True, blank=True)
    appointment_status = models.CharField(_('appointment status'), max_length=30, default='Pending', null=True, blank=True)
    appointment_approval = models.ForeignKey(AdminUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_appointments')
    appointment_rejection = models.ForeignKey(AdminUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='rejected_appointments')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('appointment')
        verbose_name_plural = _('appointments')
        ordering = ['-appointment_date']

    def __str__(self):
        return f'{self.employee} - {self.appointment_type}'

class Leave(models.Model):
    """Model for leave applications"""
    LEAVE_TYPE_CHOICES = (
        ('--Select--', _('--Select--')),
        ('Annual', _('Annual')),
        ('Vacation', _('Vacation')),
        ('Sick', _('Sick')),
        ('Maternity', _('Maternity')),
        ('Paternity', _('Paternity')),
        ('Bereavement', _('Bereavement')),
        ('Compassionate', _('Compassionate')),
        ('Study', _('Study')),
        ('Unpaid', _('Unpaid')),
        ('Other', _('Other'))
    )

    LEAVE_STATUS_CHOICES = (
        ('Pending', _('Pending')),
        ('Approved', _('Approved')),
        ('Rejected', _('Rejected')),
        ('Cancelled', _('Cancelled')),
        ('Other', _('Other'))
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves')
    leave_type = models.CharField(_('leave type'), choices=LEAVE_TYPE_CHOICES, max_length=30, null=True, blank=True)
    leave_start_date = models.DateField(_('leave start date'), null=True)
    leave_end_date = models.DateField(_('leave end date'), null=True)
    leave_duration = models.IntegerField(_('leave duration'), default=0)
    days_left = models.IntegerField(_('remaining leave days'), default=0)
    is_leave_active = models.BooleanField(default=False)
    leave_reason = models.TextField(_('leave reason'), null=True)
    leave_status = models.CharField(_('leave status'), choices=LEAVE_STATUS_CHOICES, max_length=30, default='Pending')
    leave_approval = models.ForeignKey(AdminUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    leave_rejection = models.ForeignKey(AdminUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='rejected_leaves')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('leave')
        verbose_name_plural = _('leaves')
        ordering = ['-leave_start_date']
    
    @classmethod
    def total_employees_on_leave(cls):
        active_leaves = cls.objects.filter(leave_status="Approved").values('employee').distinct().count()
        return active_leaves

    def save(self, *args, **kwargs):
        self.leave_duration = (self.leave_end_date - self.leave_start_date).days
        self.days_left = (self.leave_end_date - datetime.now().date()).days
        self.is_leave_active = self.days_left >= 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.employee} - {self.leave_type}'

class Attendance(models.Model):
    """Model for employee attendance"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(_('date'), default=datetime.now)
    time_in = models.TimeField(_('time in'), default=datetime.now)
    time_out = models.TimeField(_('time out'), default=datetime.now)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('attendance')
        verbose_name_plural = _('attendances')
        ordering = ['-date']

    def __str__(self):
        return f'{self.employee} - {self.date}'

class Payroll(models.Model):
    """Model for employee payroll"""

    PAYMENT_STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Paid', 'Paid'),
    ('Delayed', 'Delayed'),
    ('Cancelled', 'Cancelled'),
    ]


    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payrolls')
    month = models.CharField(_('month'), max_length=20, default=datetime.now().strftime('%B'))
    year = models.IntegerField(_('year'), default=datetime.now().year)
    basic_salary = models.IntegerField(_('basic salary'), default=0)
    housing_allowance = models.IntegerField(_('housing allowance'), default=0)
    transport_allowance = models.IntegerField(_('transport allowance'), default=0)
    feeding_allowance = models.IntegerField(_('feeding allowance'), default=0)
    utility_allowance = models.IntegerField(_('utility allowance'), default=0)
    other_allowance = models.IntegerField(_('other allowances'), default=0)
    total_allowance = models.IntegerField(_('total allowance'), default=0)
    tax = models.IntegerField(_('tax'), default=0)
    pension = models.IntegerField(_('pension'), default=0)
    loan = models.IntegerField(_('loan'), default=0)
    other_deductions = models.IntegerField(_('other deductions'), default=0)
    total_deductions = models.IntegerField(_('total deductions'), default=0)
    net_pay = models.IntegerField(_('net pay'), default=0)
    payment_status = models.CharField(_('payment status'), max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    
    # Attendance-related fields
    late_penalty = models.IntegerField(_('lateness penalty'), default=0)
    absent_penalty = models.IntegerField(_('absence penalty'), default=0)
    overtime_bonus = models.IntegerField(_('overtime bonus'), default=0)
    
    # Performance-related fields
    performance_bonus = models.IntegerField(_('performance bonus'), default=0)
    performance_penalty = models.IntegerField(_('performance penalty'), default=0)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('payroll')
        verbose_name_plural = _('payrolls')
        ordering = ['-year', '-month']

    def __str__(self):
        return f'{self.employee} - {self.month} {self.year}'


    def calculate_attendance_bonus(self):
        """ Logic to calculate attendance bonus based on attendance data"""
        # For example, calculate based on number of days present
        attendance_records = self.employee.attendances.filter(date__month=self.month, date__year=self.year)
        total_days = attendance_records.count()
        days_present = attendance_records.filter(time_out__isnull=False).count()
        attendance_percentage = days_present / total_days if total_days and total_days > 0 else 0
        attendance_bonus = self.employee.basic_salary * attendance_percentage * 0.05  # Assuming 5% bonus per attended day
        print(attendance_bonus)
        return attendance_bonus

    def calculate_performance_bonus(self):
        """Logic to calculate performance bonus based on performance data"""
        # For example, calculate based on average performance rating
        performance_records = self.employee.performances.filter(created_at__month=self.month, created_at__year=self.year)
        performance_ratings = [performance.performance_rating for performance in performance_records]
        average_performance_rating = mean(performance_ratings) if performance_ratings else 0
        performance_bonus = self.employee.basic_salary * (average_performance_rating / 100) * 0.1  # Assuming 10% bonus per performance rating point
        print(performance_bonus)
        return performance_bonus
    
    def calculate_other_allowances(self):
        other_allowances = self.feeding_allowance + self.transport_allowance + self.housing_allowance + self.utility_allowance + self.other_allowance
        return other_allowances

    def calculate_total_deductions(self):
        """ Logic to calculate total deductions (tax, pension, loan, etc.)"""
        total_deductions = self.tax + self.pension + self.loan + self.other_deductions
        return total_deductions

    def save(self, *args, **kwargs):
        # Calculate basic salary
        basic_salary = self.employee.basic_salary

        # Calculate allowances based on attendance and performance
        attendance_bonus = self.calculate_attendance_bonus()
        performance_bonus = self.calculate_performance_bonus()
        other_allowance = self.calculate_other_allowances()
        total_deductions = self.calculate_total_deductions()

        net_pay = basic_salary + attendance_bonus + performance_bonus + other_allowance - total_deductions

        self.basic_salary = basic_salary
        self.total_allowance = attendance_bonus + performance_bonus + other_allowance
        self.total_deductions = total_deductions
        self.net_pay = net_pay

        super().save(*args, **kwargs)


class Education(models.Model):
    """Model for employee education"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(_('institution'), max_length=100)
    course = models.CharField(_('course'), max_length=100)
    qualification = models.CharField(_('qualification'), max_length=100)
    start_date = models.DateField(_('start date'), default=datetime.now)
    end_date = models.DateField(_('end date'), default=datetime.now)
    grade = models.CharField(_('grade'), max_length=10, null=True, blank=True)
    description = models.TextField(_('description'), null=True, blank=True)
    certificate = models.FileField(_('certificate'), upload_to='employees/education_certificates/', null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('education')
        verbose_name_plural = _('education History')
        ordering = ['-end_date']

    def __str__(self):
        return f'{self.employee} - {self.qualification}'

class Training(models.Model):
    """Model for employee training"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='trainings')
    training_title = models.CharField(_('training title'), max_length=100)
    training_provider = models.CharField(_('training provider'), max_length=100, null=True, blank=True)
    training_location = models.CharField(_('training location'), max_length=100, null=True, blank=True)
    training_start_date = models.DateField(_('training start date'), null=True, blank=True)
    training_end_date = models.DateField(_('training end date'), null=True, blank=True)
    training_duration = models.IntegerField(_('training duration'), default=0, null=True, blank=True)
    training_description = models.TextField(_('training description'), null=True, blank=True)
    training_certificate = models.FileField(_('training certificate'), upload_to='employees/training_certificates/', null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('training')
        verbose_name_plural = _('trainings')
        ordering = ['-training_end_date']

    def __str__(self):
        return f'{self.employee} - {self.training_title}'

class EmployeeDocs(models.Model):
    """Model for employee documents"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='documents')
    document_name = models.CharField(_('document name'), max_length=100)
    document = models.FileField(_('document'), upload_to='employees/documents/')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')
        ordering = ['document_name', '-created_at']

    def __str__(self):
        return f'{self.employee} - {self.document_name}'
    
class Performance(models.Model):
    """Model for employee performance"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='performances')
    performance_rating = models.IntegerField(_('performance rating'), default=0)
    performance_review = models.TextField(_('performance review'))
    
    # Fields for enhanced performance tracking
    kpis = models.TextField(_('key performance indicators'), blank=True)
    self_assessment = models.TextField(_('self-assessment'), blank=True)
    manager_assessment = models.TextField(_('manager assessment'), blank=True)
    peer_feedback = models.TextField(_('peer feedback'), blank=True)
    project_performance = models.TextField(_('project performance'), blank=True)
    professional_development = models.TextField(_('professional development'), blank=True)
    improvement_plan = models.TextField(_('performance improvement plan'), blank=True)
    recognition_rewards = models.TextField(_('recognition and rewards'), blank=True)
    attendance_punctuality = models.TextField(_('attendance and punctuality'), blank=True)
    customer_feedback = models.TextField(_('customer feedback'), blank=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('performance')
        verbose_name_plural = _('performances')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.employee} - {self.performance_rating}%'

    def rank(self):
        if self.performance_rating >= 90:
            return 'Excellent'
        elif self.performance_rating >= 80:
            return 'Very Good'
        elif self.performance_rating >= 70:
            return 'Good'
        elif self.performance_rating >= 60:
            return 'Fair'
        else:
            return 'Poor' 

class WorkHistory(models.Model):
    """Model for employee work history"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='work_history')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='work_history')
    job_role = models.CharField(_('job role'), max_length=100)
    job_description = models.TextField(_('job description'))
    start_date = models.DateField(_('start date'), default=datetime.now)
    end_date = models.DateField(_('end date'), default=datetime.now)
    reason_for_leaving = models.TextField(_('reason for leaving'), null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('work history')
        verbose_name_plural = _('work Histories')
        ordering = ['-end_date']

    def __str__(self):
        return f'{self.employee} - {self.branch} - {self.job_role}'


class Finance(models.Model):
    """Model for organization financial reports"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('archived', 'Archived'),
    ]

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='finances')
    report_date = models.DateField(_('Report Date'), default=date.today)
    description = models.TextField(_('Description'), blank=True)
    created_by = models.ForeignKey('employees.AdminUser', on_delete=models.SET_NULL, null=True, related_name='owned_finances')
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='draft')
    version = models.PositiveIntegerField(_('Version'), default=1)
    comments = models.TextField(_('Comments'), blank=True)
    attachments = models.FileField(_('Attachments'), upload_to='finance_attachments/', blank=True)
    # Financial Metrics
    total_revenue = models.DecimalField(_('Total Revenue'), max_digits=15, decimal_places=2, default=0.00, blank=True)
    total_expenses = models.DecimalField(_('Total Expenses'), max_digits=15, decimal_places=2, default=0.00, blank=True)
    total_profit_loss = models.DecimalField(_('Total Profit/Loss'), max_digits=10, decimal_places=2, default=0)
    net_profit = models.DecimalField(_('Net Profit'), max_digits=15, decimal_places=2, default=0.00, blank=True)
    gross_profit = models.DecimalField(_('Gross Profit'), max_digits=15, decimal_places=2, default=0.00, blank=True)
    operating_profit = models.DecimalField(_('Operating Profit'), max_digits=15, decimal_places=2, default=0.00, blank=True)
    ebitda = models.DecimalField(_('EBITDA'), max_digits=15, decimal_places=2, default=0.00, blank=True)
    operating_expenses = models.DecimalField(_('Operating Expenses'), max_digits=15, decimal_places=2, default=0.00, blank=True)
    taxes = models.DecimalField(_('Taxes'), max_digits=15, decimal_places=2, default=0.00, blank=True)
    interest_expenses = models.DecimalField(_('Interest Expenses'), max_digits=15, decimal_places=2, default=0.00, blank=True)
    # Financial Ratios
    profit_margin = models.DecimalField(_('Profit Margin (%)'), max_digits=8, decimal_places=2, default=0.00, blank=True)
    return_on_assets = models.DecimalField(_('Return on Assets (%)'), max_digits=8, decimal_places=2, default=0.00, blank=True)
    return_on_equity = models.DecimalField(_('Return on Equity (%)'), max_digits=8, decimal_places=2, default=0.00, blank=True)
    current_ratio = models.DecimalField(_('Current Ratio'), max_digits=8, decimal_places=2, default=0.00, blank=True)
    quick_ratio = models.DecimalField(_('Quick Ratio'), max_digits=8, decimal_places=2, default=0.00, blank=True)
    debt_to_equity_ratio = models.DecimalField(_('Debt-to-Equity Ratio'), max_digits=8, decimal_places=2, default=0.00, blank=True)
    interest_coverage_ratio = models.DecimalField(_('Interest Coverage Ratio'), max_digits=8, decimal_places=2, default=0.00, blank=True)
    asset_turnover_ratio = models.DecimalField(_('Asset Turnover Ratio'), max_digits=8, decimal_places=2, default=0.00, blank=True)
    inventory_turnover_ratio = models.DecimalField(_('Inventory Turnover Ratio'), max_digits=8, decimal_places=2, default=0.00, blank=True)
    # Budget Variance Analysis
    budgeted_revenue = models.DecimalField(_('Budgeted Revenue'), max_digits=15, decimal_places=2, default=0.00, blank=True)
    budgeted_expenses = models.DecimalField(_('Budgeted Expenses'), max_digits=15, decimal_places=2, default=0.00, blank=True)
    budget_variance = models.DecimalField(_('Budget Variance'), max_digits=15, decimal_places=2, default=0.00, blank=True)
    # Forecasting
    forecasted_revenue = models.DecimalField(_('Forecasted Revenue'), max_digits=15, decimal_places=2, default=0.00, blank=True)
    forecasted_expenses = models.DecimalField(_('Forecasted Expenses'), max_digits=15, decimal_places=2, default=0.00, blank=True)
    # Audit and Logging
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Finance')
        verbose_name_plural = _('Finances')
        ordering = ['-report_date']

    def __str__(self):
        return f"{self.organization.name} - {self.report_date}"

# @receiver(pre_save, sender=Finance)
# def update_finance_totals(sender, instance, **kwargs):
#     # Calculate total income, expenses, and profit/loss
#     total_income = instance.income_items.aggregate(total=models.Sum('amount'))['total']
#     total_expenses = instance.expense_items.aggregate(total=models.Sum('amount'))['total']
#     instance.total_income = total_income if total_income is not None else 0
#     instance.total_expenses = total_expenses if total_expenses is not None else 0
#     instance.total_profit_loss = instance.total_income - instance.total_expenses