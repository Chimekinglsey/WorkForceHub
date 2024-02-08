from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group, Permission
from datetime import datetime
from organizations.models import Branch
from PIL import Image


class AdminUser(AbstractUser):
    """Custom User model for administrators"""
    employee_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(_('date of birth'), null=True, blank=True)
    # company_name = models.CharField(_('company name'), max_length=250, null=True, blank=True)
    # company_size = models.CharField(_('company size'), max_length=20, choices=COMPANY_SIZES, null=True, blank=True)
    official_email = models.EmailField(_('official email'), unique=True, null=True, blank=True)
    phone_number = models.CharField(_('phone number'), max_length=15, null=True, blank=True)
    profile_picture = models.ImageField(_('profile picture'), upload_to='adminuser/', default='default_picture.png', null=True, blank=True)
    job_role = models.CharField(_('job role'), max_length=100, null=True, blank=True)
    department_division = models.CharField(_('department/division'), max_length=100, null=True, blank=True)
    supervised_employees = models.ManyToManyField('Employee', related_name='supervisors', blank=True)
    joining_date = models.DateField(_('joining date'), default=datetime.today, null=True, blank=True)
    # manager_supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')
    groups = models.ManyToManyField( Group, verbose_name=_('groups'), blank=True, help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ), related_name='admin_users'  # Add a unique related name
    )
    user_permissions = models.ManyToManyField( Permission, verbose_name=_('user permissions'), blank=True, 
                                              help_text=_('Specific permissions for this user.'), related_name='admin_users')
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)
    class Meta:
        verbose_name = _('Administrator')
        verbose_name_plural = _('Admins')
        ordering = ['last_name', 'first_name']

class Employee(models.Model):
    """Model for employees managed by users"""
    GENDER_CHOICES = (
        ('--Select--', _('--Select--')),
        ('Male', _('Male')),
        ('Female', _('Female')),
        ('Other', _('Other'))
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

    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    adminuser = models.ForeignKey(AdminUser, on_delete=models.CASCADE, related_name='subordinates')
    # personal details
    first_name = models.CharField(_('first name'), max_length=30)
    middle_name = models.CharField(_('middle name'), max_length=30, null=True, blank=True)
    last_name = models.CharField(_('last name'), max_length=30)
    email = models.EmailField(_('email'), null=True, blank=True)
    phone_number = models.CharField(_('phone number'), max_length=15, null=True, blank=True)
    address = models.CharField(_('address'), max_length=100, null=True, blank=True)
    nationality = models.CharField(_('nationality'), max_length=30, null=True, blank=True)
    state_of_origin = models.CharField(_('state of origin'), max_length=30, null=True, blank=True)
    date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
    gender = models.CharField(_('gender'), max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    marital_status = models.CharField(_('marital status'), choices=MARITAL_STATUS_CHOICES, max_length=15, null=True, blank=True)
    profile_picture = models.ImageField(_('profile picture'), upload_to='employees/', default='default_picture.png', null=True, blank=True)
    termination_resignation_date = models.DateField(_('date of termination/resignation'), null=True, blank=True)
    emergency_contacts = models.TextField(_('emergency contacts'), null=True, blank=True)  # Store multiple contacts as JSON string or CSV 
    
    # employment details
    employee_id = models.CharField(_('employee ID'), unique=True, max_length=30)
    department = models.CharField(_('department'), max_length=30, null=True, blank=True)
    date_of_employment = models.DateField(_('date of employment'), null=True, blank=True)
    employment_status = models.CharField(_('employment status'),  choices=EMPLOYEE_STATUS_CHOICES, max_length=20, null=True, blank=True)
    employment_type = models.CharField(_('employment type'), choices=EMPLOYMENT_TYPE_CHOICES, max_length=100, null=True, blank=True)
    employee_status = models.CharField(_('employee status'),choices=EMPLOYMENT_STATUS_CHOICES,  max_length=20, null=True, blank=True)
    designation = models.CharField(_('designation'), choices=DESIGNATION_CHOICES, max_length=30, null=True, blank=True)
    level = models.CharField(_('level'), choices=LEVEL_CHOICES, max_length=30, null=True, blank=True)
    # promotion details
    last_promotion_date = models.DateField(_('last promotion date'), null=True, blank=True)
    next_promotion_date = models.DateField(_('next promotion date'), null=True, blank=True)

    # financial details
    salary = models.IntegerField(_('salary'), null=True, blank=True)
    pension_id = models.CharField(_('pension ID'), max_length=30, null=True, blank=True)
    tax_id = models.CharField(_('tax ID'), max_length=30, null=True, blank=True)
    # manager_supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')
    
    # certification details
    highest_qualification = models.CharField(_('highest qualification'), max_length=100, null=True, blank=True)
    highest_certificate = models.FileField(_('highest certificate'), upload_to='employees/highest_certificates/', null=True, blank=True)
    employment_letter = models.FileField(_('employment letter'), upload_to='employees/employment_letters/', null=True, blank=True)
    skills_qualifications = models.TextField(_('skills/qualifications'), null=True, blank=True)


    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')
        ordering = ['last_name', 'first_name']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'
    
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
    leave_start_date = models.DateField(_('leave start date'), default=datetime.now)
    leave_end_date = models.DateField(_('leave end date'), default=datetime.now)
    leave_duration = models.IntegerField(_('leave duration'), default=0)
    days_left = models.IntegerField(_('remaining leave days'), default=0)
    is_leave_active = models.BooleanField(default=False)
    leave_reason = models.TextField(_('leave reason'))
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
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payrolls')
    month = models.CharField(_('month'), max_length=20, default=datetime.now().strftime('%B'))
    year = models.IntegerField(_('year'), default=datetime.now().year)
    basic_salary = models.IntegerField(_('basic salary'), default=0)
    housing_allowance = models.IntegerField(_('housing allowance'), default=0)
    transport_allowance = models.IntegerField(_('transport allowance'), default=0)
    feeding_allowance = models.IntegerField(_('feeding allowance'), default=0)
    utility_allowance = models.IntegerField(_('utility allowance'), default=0)
    other_allowance = models.IntegerField(_('other allowance'), default=0)
    total_allowance = models.IntegerField(_('total allowance'), default=0)
    tax = models.IntegerField(_('tax'), default=0)
    pension = models.IntegerField(_('pension'), default=0)
    loan = models.IntegerField(_('loan'), default=0)
    other_deductions = models.IntegerField(_('other deductions'), default=0)
    total_deductions = models.IntegerField(_('total deductions'), default=0)
    net_pay = models.IntegerField(_('net pay'), default=0)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('payroll')
        verbose_name_plural = _('payrolls')
        ordering = ['-year', '-month']

    def __str__(self):
        return f'{self.employee} - {self.month} {self.year}'

class BankDetails(models.Model):
    """Model for employee bank details"""
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='bank_details')
    bank_name = models.CharField(_('bank name'), max_length=30, null=True, blank=True)
    account_number = models.CharField(_('account number'), max_length=30, null=True, blank=True)
    pension_id = models.CharField(_('pension ID'), max_length=30, null=True, blank=True)
    tax_id = models.CharField(_('tax ID'), max_length=30, null=True, blank=True)
    branch = models.CharField(_('branch'), max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('bank Detail')
        verbose_name_plural = _('bank Details')

    def __str__(self):
        return f'{self.employee} - {self.bank_name}'

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
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('performance')
        verbose_name_plural = _('performances')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.employee} - {self.performance_rating}'
    
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
