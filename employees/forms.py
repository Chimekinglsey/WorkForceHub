# UserCreation and ProfileUpdate forms for the AdminUser model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from employees.models import AdminUser
from organizations.models import Branch, Organization
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Div
from crispy_forms.bootstrap import TabHolder, Tab
from .models import Employee, Branch, GENDER_CHOICES, EMPLOYMENT_STATUS_CHOICES, DESIGNATION_CHOICES, NEXT_OF_KIN_RELATIONSHIP_CHOICES, EMPLOYEE_STATUS_CHOICES

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = AdminUser
        fields = ['employee_id', 'department', 'dob', 'phone_number', 'profile_picture', 
                  'job_role', 'joining_date', 'first_name', 'last_name', 'middle_name']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'required': 'true'}),
            'joining_date': forms.DateInput(attrs={'type': 'date', 'required': 'true'}),
            'employee_id': forms.TextInput(attrs={'placeholder': 'Employee ID', 'required': 'true'}),
            'department': forms.TextInput(attrs={'required': 'true'}),
            'job_role': forms.TextInput(attrs={'required': 'true'}),
            'first_name': forms.TextInput(attrs={'required': 'true'}),
            'last_name': forms.TextInput(attrs={'required': 'true'}),
            'phone_number': forms.TextInput(attrs={'required': 'true'}),
            'profile_picture': forms.FileInput(attrs={'required': 'true'}),
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

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['organization', 'name', 'location', 'email', 'contact_phone', 'contact_email', 
                  'facebook', 'twitter', 'linkedin', 'description']
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
                Column('facebook', css_class='form-group col-md-6 mb-0'),
                Column('twitter', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('linkedin', css_class='form-group col-md-6 mb-0'),
                Column('description', css_class='form-group col-md-6 mb-0', placeholder='Branch Description'),
                css_class='form-row'
            ),
            Submit('submit', 'Submit', css_class='btn btn-primary mr-5') 
        )


# Employee Detail Form
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["first_name", 'middle_name', 'last_name', 'phone_number', 'dob', 'gender', 'email', 'profile_picture',
                  'employee_id', 'branch', 'department', 'job_role', 'joining_date', 'next_of_kin_name', 'next_of_kin_relationship',
                  'next_of_kin_phone_number', 'next_of_kin_address', 'emergency_contacts',
                  'highest_qualification', 'highest_certificate', 'employment_letter', 'skills_qualifications',
                  'employment_status', 'employment_type', 'designation', 'adminuser']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
            'emergency_contacts': forms.Textarea(attrs={'rows': 2}),
            'skills_qualifications': forms.Textarea(attrs={'rows': 2}),
        }
        

    def __init__(self, organization, adminuser, *args, **kwargs):
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
                    'Next of Kin',
                    Row(
                        Column('next_of_kin_name', css_class='form-group col-md-6 mb-0'),
                        Column('next_of_kin_relationship', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('next_of_kin_phone_number', css_class='form-group col-md-6 mb-0'),
                        Column('next_of_kin_address', css_class='form-group col-md-6 mb-0'),
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
        self.fields['branch'].queryset = Branch.objects.filter(organization=organization)
        self.fields['branch'].empty_label = 'Select Branch'
        self.fields['adminuser'].queryset = AdminUser.objects.filter(pk=organization.admin_user.id)       
        self.fields['gender'].choices = GENDER_CHOICES
        self.fields['employment_status'].choices = EMPLOYMENT_STATUS_CHOICES
        self.fields['employment_type'].choices = EMPLOYEE_STATUS_CHOICES
        self.fields['designation'].choices = DESIGNATION_CHOICES
        self.fields['next_of_kin_relationship'].choices = NEXT_OF_KIN_RELATIONSHIP_CHOICES
        self.fields['joining_date'].label = 'Date Employed'