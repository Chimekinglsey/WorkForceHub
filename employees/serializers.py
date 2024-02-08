from rest_framework import serializers
from .models import Employee, AdminUser
from organizations.models import Branch


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())
    adminuser = serializers.HyperlinkedRelatedField(view_name='adminuser-detail', read_only=True)
    class Meta:
        model = Employee
        fields = ('id', 'url', 'employee_id', 'last_name', 'first_name', 'email',
                  'branch', 'department', 'level','adminuser')

class AdminUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AdminUser
        fields = ('id','url', 'employee_id', 'username','email', 'first_name', 'last_name',  'is_staff', 'is_superuser')

