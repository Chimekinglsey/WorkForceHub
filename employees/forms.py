# UserCreation and ProfileUpdate forms for the AdminUser model
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm
from employees.models import AdminUser, Payroll
from organizations.models import Branch, Organization,Transfer, OrgDocuments as OrgDocs
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Div, Fieldset, Field
from crispy_forms.bootstrap import TabHolder, Tab
from .models import Employee, Branch, GENDER_CHOICES, EMPLOYMENT_STATUS_CHOICES, DESIGNATION_CHOICES, NEXT_OF_KIN_RELATIONSHIP_CHOICES, EMPLOYEE_STATUS_CHOICES
from .models import Performance


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

    class Meta:
        model = AdminUser
        fields = ('branch', 'email', 'username', 'password1', 'password2', 'first_name','middle_name', 'last_name', 'can_change_password')

    def __init__(self, organization, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['branch'].queryset = Branch.objects.filter(organization=organization)
        self.fields['branch'].empty_label = 'Select Branch'
        self.fields['can_change_password'].required = True
        self.fields['can_change_password'].label = 'Can Change Password?'

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('middle_name', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('branch', css_class='form-group col-md-6 mb-0'),
                Column('username', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('can_change_password', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Submit('submit', 'Submit', css_class='btn btn-primary'),
                css_class='btnHandle'
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


# Organizations branch form
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
                  'next_of_kin_phone_number', 'emergency_contacts',
                  'highest_qualification', 'highest_certificate', 'employment_letter', 'skills_qualifications',
                  'employment_status', 'employment_type', 'designation', 'adminuser', 'bank_name', 'account_number', 'account_name',
                  'pension_id', 'tax_id'
                  ]
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
        self.fields['branch'].queryset = Branch.objects.filter(organization=organization)
        self.fields['branch'].empty_label = 'Select Branch'
        # self.fields['adminuser'].queryset = AdminUser.objects.filter(pk=organization.admin_user.id)       
        self.fields['adminuser'].queryset = AdminUser.objects.filter(pk=adminuser.id)       
        self.fields['gender'].choices = GENDER_CHOICES
        self.fields['employment_status'].choices = EMPLOYMENT_STATUS_CHOICES
        self.fields['employment_type'].choices = EMPLOYEE_STATUS_CHOICES
        self.fields['designation'].choices = DESIGNATION_CHOICES
        self.fields['next_of_kin_relationship'].choices = NEXT_OF_KIN_RELATIONSHIP_CHOICES
        self.fields['joining_date'].label = 'Date Employed'


# Payroll form
class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = '__all__'

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
        fields = ['performance_review', 'performance_rating']
        widgets = {
            'performance_review': forms.Textarea(attrs={'rows': 4}),
            'performance_rating': forms.NumberInput(attrs={'type': 'number', 'min': 0, 'max': 100, 'title': 'Rate the employee performance between 0-100'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Performance Review',
                Row(
                    Column('performance_review', css_class='form-group col-md-12'),
                    Column('performance_rating', css_class='form-group col-md-12'),
                    css_class='form-row'
                ),
                Row(
                    Column(Submit('submit', 'Submit', css_class='btn btn-primary ml-auto mb-5')),
                    css_class='btnHandle'
                )
            )
        )


class ProjectPerformanceForm(forms.ModelForm):
    class Meta:
        model = Performance
        fields = ['project_performance', 'customer_feedback', 'manager_assessment', 'peer_feedback']
        widgets = {
            'project_performance': forms.Textarea(attrs={'rows': 4}),
            'customer_feedback': forms.Textarea(attrs={'rows': 4}),
            'manager_assessment': forms.Textarea(attrs={'rows': 4}),
            'peer_feedback': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Performance Feedback',
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
                    Column(Submit('submit', 'Submit', css_class='btn btn-primary ml-auto mb-5')),
                    css_class='btnHandle'
                ),
            )
        )
        

# other performance forms
        
class OtherPerformanceForm(forms.ModelForm):
    class Meta:
        model = Performance
        fields = ['kpis', 'self_assessment','professional_development', 
                  'improvement_plan', 'recognition_rewards', 
                  'attendance_punctuality']
        widgets = {
            'professional_development': forms.Textarea(attrs={'rows': 4}),
            'improvement_plan': forms.Textarea(attrs={'rows': 4}),
            'kpis': forms.Textarea(attrs={'rows': 4}),
            'self_assessment': forms.Textarea(attrs={'rows': 4}),
            'recognition_rewards': forms.Textarea(attrs={'rows': 4}),
            'attendance_punctuality': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Performance Feedback',
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
        fields = ['employee', 'source_branch', 'destination_branch', 'reason']

    def __init__(self, organization, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter source branch based on organization and current user
        self.fields['source_branch'].queryset = Branch.objects.filter(organization=organization)
        self.fields['source_branch'].disabled = True
        self.fields['source_branch'].required = False
        self.fields['destination_branch'].queryset = Branch.objects.filter(organization=organization)
        self.fields['reason'].widget.attrs={'rows': 4}

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
            