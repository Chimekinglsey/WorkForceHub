from rest_framework import viewsets, views
from .serializers import OrganizationSerializer
from .models import Organization
from .permissions import IsAdminUser, IsSafeOrPutOnly, IsAuthenticated, IsOrgAdmin
from rest_framework.response import Response
from rest_framework.reverse import reverse


class WorkforceHubAPI(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = {}
        if request.user.is_superuser:
            data['employees'] = reverse('employees-list', request=request)
            data['admin_users'] = reverse('admin_users-list', request=request)
            data['organizations'] = reverse('organizations-list', request=request)
        elif request.user.is_delegate:
            data['employees'] = reverse('employees-list', request=request)
        return Response(data)

class OrganizationViewSet(viewsets.ModelViewSet):
    """ View or modify an organization """
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated, IsOrgAdmin, IsSafeOrPutOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Organization.objects.filter(admin_user=user.adminuser)
        return Organization.objects.none()
