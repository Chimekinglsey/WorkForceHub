from rest_framework import serializers
from .models import Organization
from employees.models import AdminUser

class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    admin_user = serializers.PrimaryKeyRelatedField(queryset=AdminUser.objects.none())

    class Meta:
        model = Organization
        fields = ('id', 'url', 'admin_user', 'name', 'industry', 'sector', 'headquarter', 'size',
                  'website', 'contact_email', 'created_at')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        # if request and request.user.is_superuser:
        #     self.fields['admin_user'].queryset = AdminUser.objects.filter(id=request.user.adminuser.branch.organization)
        # else:
        #     self.fields['admin_user'].queryset = AdminUser.objects.filter(branch=request.user.adminuser.branch)
        self.fields['admin_user'].queryset = AdminUser.objects.filter(id=request.user.id)


        











# Compare this snippet from WorkForceHub/employees/views.py: