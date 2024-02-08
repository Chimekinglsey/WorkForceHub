from rest_framework import viewsets, permissions
from .serializers import OrganizationSerializer
from .models import Organization
from .permissions import IsAdminUser


class OrganizationViewSet(viewsets.ModelViewSet):
    """ View or modify an organization """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class OrganizationDetailViewSet(viewsets.ModelViewSet):
    """ View or modify an organization """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminUser]
