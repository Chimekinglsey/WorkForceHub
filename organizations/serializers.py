from rest_framework import serializers
from .models import Organization

class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'url', 'name','industry', 'sector', 'headquarter', 'size',
                  'website','contact_email', 'created_at')