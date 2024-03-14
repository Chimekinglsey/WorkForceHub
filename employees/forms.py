# UserCreation and ProfileUpdate forms for the AdminUser model
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm
from employees.models import AdminUser, Payroll, Finance
from organizations.models import Branch, Organization,Transfer, OrgDocuments as OrgDocs, Report
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Div, Fieldset, Field, Button
from crispy_forms.bootstrap import TabHolder, Tab
from .models import Employee, Branch, GENDER_CHOICES, EMPLOYMENT_STATUS_CHOICES, DESIGNATION_CHOICES, NEXT_OF_KIN_RELATIONSHIP_CHOICES, EMPLOYEE_STATUS_CHOICES
from .models import Performance
from datetime import datetime


# This method validates image file
def validate_image_extension(value):
    if not value.name.endswith(('.jpeg', '.jpg', '.JPEG', '.JPG', '.PNG', '.png')):
        raise ValidationError('Only .jpeg, .jpg, .JPEG, .JPG, .PNG, .png formats are supported.')


# UserCreation form for the AdminUser model
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required. Enter a valid email address.',
                             widget=forms.TextInput(attrs={'placeholder': 'Enter your email', 'autofocus': 'true'}))
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = AdminUser
        fields = ('email', 'username', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long")
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class DelegateAdminCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Enter a valid email address.')
    username = forms.CharField(max_length=30)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(),help_text='Must contain at least 8 characters, including alphanumeric and a special character')
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(), help_text='Enter the same password as before, for validation.')
    branch = forms.ModelChoiceField(queryset=Branch.objects.none())  # Initialize queryset as empty
    can_change_password = forms.ChoiceField(
        label='Can change password?',
        choices=[(True, 'Yes'), (False, 'No')],
        initial=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Can the delegate change their password?'
    )
    class Meta:
        model = AdminUser
        fields = ('branch', 'email', 'username', 'password1', 'password2', 'first_name', 'last_name', 'can_change_password')

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control validateEmail'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control validatePassword'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control validatePassword1'}),
        }
    def __init__(self, organization, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['branch'].queryset = Branch.objects.filter(organization=organization)
        self.fields['branch'].empty_label = 'Select Branch'
        self.fields['can_change_password'].required = True
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('branch', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('password1', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('password2', css_class='form-group col-md-6 mb-0'),
                Column('can_change_password', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
            Button('back', 'Back', css_class='btn btn-danger mr-5 backBtn'),
            Submit('submit', 'Submit', css_class='btn btn-primary mr-5'),
            css_class='btnHandle2'
            )
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# ProfileUpdate form for the AdminUser model
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = AdminUser
        fields = ['employee_id', 'department', 'dob', 'phone_number', 'profile_picture', 
                  'job_role', 'joining_date', 'first_name', 'last_name', 'middle_name']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'placeholder': 'DD/MM/YYYY'}),
            'joining_date': forms.DateInput(attrs={'type': 'date', 'max': datetime.now().strftime('%Y-%m-%d'), 'placeholder': 'DD/MM/YYYY'}),
            'phone_number': forms.TextInput(attrs={'type': 'tel', 'placeholder': 'e.g +2347008009000'}),
            'employee_id': forms.TextInput(attrs={'placeholder': 'Employee ID', 'title': 'Override the employee ID if necessary'}),
        }
    profile_picture = forms.ImageField(validators=[validate_image_extension])
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Personal Information',
                    Row(
                        Column('first_name', css_class='form-group col-md-6 mb-0'),
                        Column('middle_name', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('last_name', css_class='form-group col-md-6 mb-0'),
                        Column('phone_number', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    
                    Row(
                        Column('dob', css_class='form-group col-md-6 mb-0', type='date', placeholder='Date of Birth'),
                        Column('profile_picture', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                ),
                Tab(
                    'Employment Details',
                    Row(
                        Column('employee_id', css_class='form-group col-md-6 mb-0'),
                        Column('department', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('job_role', css_class='form-group col-md-6 mb-0'),
                        Column('joining_date', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Submit('submit', 'Submit', css_class='btn btn-primary mr-5') 
                ),
            )
        )
        self.fields['dob'].required = True
        self.fields['employee_id'].required = True
        self.fields['department'].required = True
        self.fields['job_role'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['phone_number'].required = True
        self.fields['profile_picture'].required = True
        self.fields['dob'].label = 'Date of Birth'
        self.fields['joining_date'].label = 'Date Employed'
        self.fields['employee_id'].label = 'Employee ID'
        self.fields['department'].label = 'Department'
        self.fields['job_role'].label = 'Job Role'
        self.fields['profile_picture'].label = 'Profile Picture'
        self.fields['phone_number'].label = 'Phone Number'
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['middle_name'].label = 'Middle Name'

# Organizations branch form
class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['organization', 'name', 'location', 'email', 'contact_phone', 'contact_email', 
                  'facebook', 'twitter', 'linkedin', 'description']
        widget = {
            'contact_phone': forms.TextInput(attrs={'type': 'tel', 'placeholder': 'e.g +2347008009000'}),
            'contact_email': forms.EmailInput(attrs={'placeholder': 'e.g abc@example.com'}),
        }
    def __init__(self, user, *args, **kwargs):
        super(BranchForm, self).__init__(*args, **kwargs)
        self.fields['organization'].queryset = Organization.objects.filter(admin_user=user)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('organization', css_class='form-group col-md-6 mb-0'),
                Column('name', css_class='form-group col-md-6 mb-0', placeholder='Branch Name'),
                css_class='form-row'
            ),
            Row(
                Column('location', css_class='form-group col-md-6 mb-0', placeholder='Branch Location'),
                Column('email', css_class='form-group col-md-6 mb-0', placeholder='Branch Email'),
                css_class='form-row'
            ),
            Row(
                Column('contact_phone', css_class='form-group col-md-6 mb-0', type='tel', placeholder='Contact Person Phone'),
                Column('contact_email', css_class='form-group col-md-6 mb-0', type='email', placeholder='Contact Person Email'),
                css_class='form-row'
            ),
            Row(
                Column('facebook', css_class='form-group col-md-6 mb-0 presignedUrl'),
                Column('twitter', css_class='form-group col-md-6 mb-0 presignedUrl'),
                css_class='form-row'
            ),
            Row(
                Column('linkedin', css_class='form-group col-md-6 mb-0 presignedUrl'),
                Column('description', css_class='form-group col-md-6 mb-0', placeholder='Branch Description'),
                css_class='form-row'
            ),
            Row(
            Button('back', 'Back', css_class='btn btn-danger mr-5 backBtn'),
            Submit('submit', 'Submit', css_class='btn btn-primary mr-5'),
            css_class='btnHandle2'
            )
        )
        self.fields['name'].label = 'Branch Name'
        self.fields['location'].label = 'Branch Location'
        self.fields['email'].label = 'Branch Email'
        self.fields['contact_phone'].label = 'Contact Person Phone'
        self.fields['contact_email'].label = 'Contact Person Email'
        self.fields['description'].label = 'Branch Description'
        # set description rows to 2
        self.fields['description'].widget.attrs['rows'] = 2
        # prepend https:// to the social media fields
        self.fields['facebook'].widget.attrs['value'] = 'https://facebook.com/yourpage'
        self.fields['twitter'].widget.attrs['value'] = 'https://x.com/yourpage'
        self.fields['linkedin'].widget.attrs['value'] = 'https://linkedin.com/in/yourpage'



# Employee Detail Form
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["first_name", 'middle_name', 'last_name', 'phone_number', 'dob', 'gender', 'email', 'profile_picture',
                  'employee_id', 'branch', 'department', 'job_role', 'joining_date', 'next_of_kin_name', 'next_of_kin_relationship',
                  'next_of_kin_phone_number', 'emergency_contacts',
                  'highest_qualification', 'highest_certificate', 'employment_letter', 'skills_qualifications',
                  'employment_status', 'employment_type', 'designation', 'adminuser', 'bank_name', 'account_number', 'account_name',
                  'pension_id', 'tax_id'
                  ]
        # include fa icons in the placeholders  
        widgets = {
            'phone_number': forms.TextInput(attrs={'type': 'tel', 'placeholder': 'e.g +2347008009000'}),
            'email': forms.EmailInput(attrs={'placeholder': 'e.g abc@example.com'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'placeholder': 'DD/MM/YYYY'}),
            'joining_date': forms.DateInput(attrs={'type': 'date', 'max': datetime.now().strftime('%Y-%m-%d')}),
            'next_of_kin_phone_number': forms.TextInput(attrs={'type': 'tel'}),
            'emergency_contacts': forms.Textarea(attrs={'rows': 2}),
            'skills_qualifications': forms.Textarea(attrs={'rows': 2}),
        }
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Personal Information',
                    Row(
                        Column('first_name', css_class='form-group col-md-6 mb-0'),
                        Column('middle_name', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),

                    Row(
                        Column('last_name', css_class='form-group col-md-6 mb-0'),
                        Column('phone_number', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('dob', css_class='form-group col-md-6 mb-0', placeholder='Date of Birth'),
                        Column('gender', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('email', css_class='form-group col-md-6 mb-0', placeholder='Email Address'),
                        Column('profile_picture', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                        ),
                ),
                Tab(
                    'Employment Details',
                    Row(
                        Column('employee_id', css_class='form-group col-md-6 mb-0'),
                        Column('branch', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('department', css_class='form-group col-md-6 mb-0'),
                        Column('job_role', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('employment_type', css_class='form-group col-md-6 mb-0'),
                        Column('employment_status', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('designation', css_class='form-group col-md-6 mb-0'),
                        Column('joining_date', css_class='form-group col-md-6 mb-0', placeholder='Date Employed'),
                        css_class='form-row'
                    ),
                ),
                Tab(
                    'Bank Details and Next of Kin',
                    Row(
                        Column('bank_name', css_class='form-group col-md-6 mb-0'),
                        Column('account_number', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('account_name', css_class='form-group col-md-6 mb-0'),
                        Column('pension_id', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('tax_id', css_class='form-group col-md-6 mb-0'),
                        Column('next_of_kin_name', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('next_of_kin_relationship', css_class='form-group col-md-6 mb-0'),
                        Column('next_of_kin_phone_number', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                ),
                Tab(
                    'Other Information',
                    Row(
                        Column('emergency_contacts', css_class='form-group col-md-6 mb-0'),
                        Column('adminuser', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('highest_qualification', css_class='form-group col-md-6 mb-0'),
                        Column('highest_certificate', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('employment_letter', css_class='form-group col-md-6 mb-0'),
                        Column('skills_qualifications', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                Div(
                    Submit('submit', 'Submit', css_class='btn btn-primary mr-5'),
                    css_class='text-right, btnHandle'
                )
                ),
            )
        )
        # Filter branches based on organization
        # self.fields['branch'].queryset = Branch.objects.filter(organization=organization)
        self.fields['branch'].empty_label = 'Branch'
        self.fields['branch'].required = False
        self.fields['branch'].disabled = True
        # self.fields['adminuser'].queryset = AdminUser.objects.filter(pk=organization.admin_user.id)       
        # self.fields['adminuser'].queryset = AdminUser.objects.filter(pk=adminuser.id)
        self.fields['adminuser'].label = 'Admin'       
        self.fields['adminuser'].required = False
        self.fields['adminuser'].disabled = True
        self.fields['gender'].choices = GENDER_CHOICES
        self.fields['employment_status'].choices = EMPLOYMENT_STATUS_CHOICES
        self.fields['employment_type'].choices = EMPLOYEE_STATUS_CHOICES
        self.fields['designation'].choices = DESIGNATION_CHOICES
        self.fields['next_of_kin_relationship'].choices = NEXT_OF_KIN_RELATIONSHIP_CHOICES
        self.fields['joining_date'].label = 'Date Employed'
        self.fields['employee_id'].required = True


# Payroll form
class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = '__all__'

    # set this year as default value
        initial = {'year': datetime.now().year, 'month': datetime.now().month}
        widgets = {
            'year': forms.NumberInput(attrs={'type': 'number', 'min': 1900, 'max': datetime.now().year}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Payroll Information',
                Row(
                    Column('employee', css_class='form-group col-md-6 mb-0'),
                    Column('month', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('year', css_class='form-group col-md-6 mb-0'),
                    Column('basic_salary', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('housing_allowance', css_class='form-group col-md-6 mb-0'),
                    Column('transport_allowance', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('feeding_allowance', css_class='form-group col-md-6 mb-0'),
                    Column('utility_allowance', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('other_allowance', css_class='form-group col-md-6 mb-0'),
                    Column('total_allowance', css_class='form-group col-md-6 mb-0', title='Calculated automatically'),
                    css_class='form-row'
                ),
                Row(
                    Column('tax', css_class='form-group col-md-6 mb-0'),
                    Column('pension', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('loan', css_class='form-group col-md-6 mb-0'),
                    Column('other_deductions', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('total_deductions', css_class='form-group col-md-6 mb-0', title='Calculated automatically'),
                    Column('performance_penalty', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('late_penalty', css_class='form-group col-md-6 mb-0'),
                    Column('absent_penalty', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('overtime_bonus', css_class='form-group col-md-6 mb-0'),
                    Column('performance_bonus', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('net_pay', css_class='form-group col-md-6 mb-0', title='Calculated automatically'),
                    Column('payment_status',  css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Submit('submit', 'Update', css_class='btn btn-primary mr-2'), 
                    css_class='btnHandle'
                ),
            ),
        )        


#  Performance forms
class PerformanceReviewForm(forms.ModelForm):
    class Meta:
        model = Performance
        fields = ['performance_review', 'performance_rating', 'project_performance', 'customer_feedback', 
                  'manager_assessment', 'peer_feedback', 'kpis', 'self_assessment','professional_development', 
                  'improvement_plan', 'recognition_rewards', 'attendance_punctuality'
                  ]
        widgets = {
            'performance_review': forms.Textarea(attrs={'rows': 2}),
            'performance_rating': forms.NumberInput(attrs={'type': 'number', 'min': 0, 'max': 100, 'help_text': 'Rate the employee performance between 0-100'}),
            'project_performance': forms.Textarea(attrs={'rows': 2}),
            'customer_feedback': forms.Textarea(attrs={'rows': 2}),
            'manager_assessment': forms.Textarea(attrs={'rows': 2}),
            'peer_feedback': forms.Textarea(attrs={'rows': 2}),
            'professional_development': forms.Textarea(attrs={'rows': 2}),
            'improvement_plan': forms.Textarea(attrs={'rows': 2}),
            'kpis': forms.Textarea(attrs={'rows': 2}),
            'self_assessment': forms.Textarea(attrs={'rows': 2}),
            'recognition_rewards': forms.Textarea(attrs={'rows': 2}),
            'attendance_punctuality': forms.Textarea(attrs={'rows': 2}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Performance Review',
                Row(
                    Column('performance_review', css_class='form-group col-md-6 mb-0'),
                    Column('performance_rating', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('project_performance', css_class='form-group col-md-6 mb-0'),
                    Column('customer_feedback', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'

                ),
                Row(
                    Column('manager_assessment', css_class='form-group col-md-6 mb-0'),
                    Column('peer_feedback', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('professional_development', css_class='form-group col-md-6 mb-0'),
                    Column('improvement_plan', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('kpis', css_class='form-group col-md-6 mb-0'),
                    Column('self_assessment', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('recognition_rewards', css_class='form-group col-md-6 mb-0'),
                    Column('attendance_punctuality', css_class='form-group col-md-6 mb-0'),
                ),
                Row(
                    Column(Submit('submit', 'Submit', css_class='btn btn-primary ml-auto mb-5')),
                    css_class='btnHandle'
                )

            )
        )
        self.fields['performance_review'].label = 'Overall Performance Review'
        self.fields['performance_review'].help_text = 'This is the overall performance review of the employee. It should be a summary of the employee\'s performance for the period.'
        self.fields['performance_rating'].label = 'Overall Performance Rating'
        self.fields['performance_rating'].help_text = 'Rate the employee performance between 0-100'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = AdminUser
        fields = ['first_name', 'last_name', 'email', 'profile_picture']
        widgets = {
            # first_name and last_name are read-only fields
            'first_name': forms.TextInput(attrs={'readonly': 'true'}),
            'last_name': forms.TextInput(attrs={'readonly': 'true'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'profile_picture': forms.FileInput(attrs={'required': 'true'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                '',
                Row(
                    Column('first_name', css_class='form-group col-md-6 mb-0'),
                    Column('last_name', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('email', css_class='form-group col-md-6 mb-0'),
                    Column('profile_picture', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column(Submit('submit', 'Submit', css_class='btn btn-primary ml-auto mb-5')),
                    css_class='btnHandle'
                )
            )
        )

class ChangePasswordForm(PasswordChangeForm):
    # inlcude fa icons in the placeholders
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                Row(
                    Column('old_password', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row flex-center'
                ),
                Row(
                    Column('new_password1', css_class='form-group col-md-6 mb-0'),
                    Column('new_password2', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column(Submit('submit', 'Submit', css_class='btn btn-primary mb-5')),
                    css_class='btnHandle'
                )
            )
        )
        self.helper.form_method = 'post'
        
class BranchDocumentsForm(forms.ModelForm):
    class Meta:
        model = OrgDocs
        fields = ['document_name', 'document']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                '',
                Row(
                    Column('document_name', css_class='form-group col-md-6 mb-0'),
                    Column('document', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column(Submit('submit', 'Submit', css_class='btn btn-primary ml-auto mb-5')),
                    css_class='btnHandle'
                )
            )
        )
        self.fields['document_name'].required = True
        self.fields['document'].required = True
        self.fields['document_name'].label = 'Document Title'
        self.fields['document'].label = 'Document'
        self.fields['document'].help_text = 'Select a document to Upload'
        self.fields['document'].widget.attrs['accept'] = '.pdf, .doc, .docx, .xls, .xlsx, .ppt, .pptx, .txt'

# Transfer form
class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['organization', 'employee', 'source_branch', 'destination_branch', 'reason']

    def __init__(self, organization, adminuser, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter source branch based on organization and current user
        self.fields['source_branch'].queryset = Branch.objects.filter(organization=organization)
        self.fields['source_branch'].disabled = True
        self.fields['source_branch'].required = False
        self.fields['organization'].required = False
        self.fields['destination_branch'].queryset = Branch.objects.filter(organization=organization)
        self.fields['reason'].widget.attrs={'rows': 4}
        # only employees in a particular branch should be in the queryset
        self.fields['employee'].queryset = Employee.objects.filter(branch=adminuser.branch)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('employee', css_class='form-control'),
                    css_class='col-md-6'
                ),
                Div(
                    Field('source_branch', css_class='form-control'),
                    css_class='col-md-6'
                ),
                    css_class='row form-row'
            ),
            Div(
                Div(
                    Field('destination_branch', css_class='form-control'),
                    css_class='col-md-6'
                ),
                Div(
                    Field('reason', css_class='form-control'),
                    css_class='col-md-6'
                ),
                css_class='row form-row'
            ),
            Submit('submit', 'Submit', css_class='btn btn-primary')
        )

# Branch reports form
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'branch', 'report_date', 'description', 'status', 'comments',
                'attachments', 'created_by', 'report_type', 'category']
        # include fa icons in the placeholders
        widgets = {
            'report_date': forms.DateInput(attrs={'type': 'date', 'placeholder': "DD/MM/YYYY"}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'comments': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Report Form',
                Row(
                    Column('title', css_class='form-group col-md-6 mb-0'),
                    Column('branch', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('report_type', css_class='form-group col-md-6 mb-0'),
                    Column('category', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('description', css_class='form-group col-md-6 mb-0'),
                    Column('attachments', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('report_date', css_class='form-group col-md-6 mb-0'),
                    Column('status', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('comments', css_class='form-group col-md-6 mb-0'),
                    Column('created_by', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column(Submit('submit', 'Submit', css_class='btn btn-primary ml-auto mb-5')),
                    css_class='btnHandle'
                )
            )
        )
        self.fields['title'].required = True
        self.fields['branch'].disabled = True
        self.fields['branch'].required = False
        self.fields['created_by'].disabled = True
        self.fields['created_by'].required = False

class BasicFinanceForm(forms.ModelForm):
    class Meta:
        model = Finance
        fields = ['branch', 'report_date', 'total_revenue', 'total_expenses', 'created_by', 'status', 'description', 'attachments']
    
        widgets = {
            'report_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Basic Financial Information',
                Row(
                    Column('branch', css_class='form-group col-md-6 mb-0'),
                    Column('report_date', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('total_revenue', css_class='form-group col-md-6 mb-0'),
                    Column('total_expenses', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('created_by', css_class='form-group col-md-6 mb-0'),
                    Column('status', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('description', css_class='form-group col-md-6 mb-0'),
                    Column('attachments', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column(Submit('submit', 'Submit', css_class='btn btn-primary ml-auto mb-5')),
                    css_class='btnHandle'
                )
            )
        )

        self.fields['branch'].disabled = True
        self.fields['branch'].required = False
        self.fields['created_by'].disabled = True
        self.fields['created_by'].required = False
        self.fields['report_date'].widget.attrs['type'] = 'date'
        self.fields['report_date'].required = True

class DetailedFinanceForm(forms.ModelForm):
    """This form is used to capture detailed financial information"""
    class Meta:
        model = Finance
        fields = ['branch', 'report_date', 'total_revenue', 'total_expenses', 'created_by', 'status', 'description',
                    'attachments', 'total_profit_loss', 'net_profit', 'gross_profit', 'operating_profit', 'ebitda',
                    'operating_expenses', 'taxes', 'interest_expenses', 'profit_margin', 'return_on_assets', 'return_on_equity',
                    'current_ratio', 'quick_ratio', 'debt_to_equity_ratio', 'interest_coverage_ratio', 'asset_turnover_ratio',
                    'inventory_turnover_ratio', 'budgeted_revenue', 'budgeted_expenses', 'budget_variance', 'forecasted_revenue',
                    'forecasted_expenses', 'comments'
                    ]
                    
        widgets = {
            'report_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 2}),
            'comments': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Basic Financial Information',
                    Row(
                        Column('branch', css_class='form-group col-md-6 mb-0'),
                        Column('report_date', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('total_revenue', css_class='form-group col-md-6 mb-0'),
                        Column('total_expenses', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('created_by', css_class='form-group col-md-6 mb-0'),
                        Column('status', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('description', css_class='form-group col-md-6 mb-0'),
                        Column('attachments', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                ),
                Tab(
                    'Financial Metrics',
                    Row(
                        Column('net_profit', css_class='form-group col-md-6 mb-0'),
                        Column('gross_profit', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('operating_profit', css_class='form-group col-md-6 mb-0'),
                        Column('ebitda', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('operating_expenses', css_class='form-group col-md-6 mb-0'),
                        Column('taxes', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('interest_expenses', css_class='form-group col-md-6 mb-0'),
                        Column('total_profit_loss', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                ),
                Tab(
                    'Financial Ratios',
                    Row(
                        Column('profit_margin', css_class='form-group col-md-6 mb-0'),
                        Column('return_on_assets', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('return_on_equity', css_class='form-group col-md-6 mb-0'),
                        Column('current_ratio', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),

                    Row(
                        Column('quick_ratio', css_class='form-group col-md-6 mb-0'),
                        Column('debt_to_equity_ratio', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('interest_coverage_ratio', css_class='form-group col-md-6 mb-0'),
                        Column('asset_turnover_ratio', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('inventory_turnover_ratio', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                ),
                Tab(
                    'Budget and Forecast',
                    Row(
                        Column('budgeted_revenue', css_class='form-group col-md-6 mb-0'),
                        Column('budgeted_expenses', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('budget_variance', css_class='form-group col-md-6 mb-0'),
                        Column('forecasted_revenue', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('forecasted_expenses', css_class='form-group col-md-6 mb-0'),
                        Column('comments', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column(Submit('submit', 'Submit', css_class='btn btn-primary ml-auto mb-5')),
                        css_class='btnHandle'
                    )
                )
            )
        )
        self.fields['branch'].disabled = True
        self.fields['branch'].required = False
        self.fields['created_by'].disabled = True
        self.fields['created_by'].required = False

