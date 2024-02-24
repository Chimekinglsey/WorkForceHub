from rest_framework import serializers
from .models import Employee, AdminUser
from organizations.models import Branch

class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())
    adminuser = serializers.HyperlinkedRelatedField(view_name='adminuser-detail', read_only=True)
    class Meta:
        model = Employee
        fields = ('id', 'url', 'branch', 'employee_id', 'email', 'first_name', 'middle_name',
                   'last_name', 'phone_number', 'dob', 'gender', 'marital_status', 'address', 'nationality',
                   'state_of_origin', 'department', 'job_role', 'joining_date', 'employment_type', 'employment_status',
                   'designation', 'level', 'last_promotion_date', 'next_promotion_date', 'basic_salary', 'emergency_contacts',
                   'termination_resignation_date', 'highest_qualification','profile_picture', 'highest_certificate', 'employment_letter',
                   'skills_qualifications', 'next_of_kin_name', 'next_of_kin_relationship', 'next_of_kin_phone_number',
                    'supervised_employees', 'created_at', 'updated_at', 'adminuser', 'bank_name', 'account_number',
                   'account_name', 'pension_id', 'tax_id',
                   )

class AdminUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AdminUser
        fields = ('id','url', 'employee_id', 'username','email', 'first_name', 'last_name',  'is_staff', 'is_superuser')

