# UserCreation and ProfileUpdate forms for the AdminUser model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from employees.models import AdminUser
from organizations.models import Branch, Organization
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from crispy_forms.bootstrap import TabHolder, Tab


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = AdminUser
        fields = ['employee_id', 'department', 'dob', 'phone_number', 'profile_picture', 
                  'job_role', 'joining_date', 'first_name', 'last_name', 'middle_name']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
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
                        Column('dob', css_class='form-group col-md-6 mb-0'),
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