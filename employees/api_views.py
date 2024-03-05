from django.http import HttpResponse
from rest_framework import viewsets, generics, permissions
from .serializers import EmployeeSerializer, AdminUserSerializer
from .models import Employee, AdminUser
from .permissions import IsAdminUser, IsBranchAdmin, IsMasterAdmin

def home(request):
    return HttpResponse("Welcome to WorkforceHub")

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows employees to be viewed or edited.
    """
    serializer_class = EmployeeSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsBranchAdmin]
        else:
            permission_classes = [IsBranchAdmin | IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Employee.objects.filter(branch__organization=self.request.user.branch.organization)
            return queryset
        return Employee.objects.filter(branch=self.request.user.branch)

class EmployeeDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    """ API endpoint that allows detailed view and update of employee"""
    serializer_class = EmployeeSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsBranchAdmin]
        else:
            permission_classes = [IsBranchAdmin | IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """ Get the queryset for the view. This is overriden to filter based on the user's organization """
        if self.request.user.is_superuser:
            return Employee.objects.filter(branch__organization=self.request.user.adminuser.branch.organization)
        return Employee.objects.filter(branch=self.request.user.branch) 



class AdminUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin users to be viewed or edited.
    """
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return AdminUser.objects.filter(branch__organization=self.request.user.adminuser.branch.organization)
        return AdminUser.objects.filter(branch=self.request.user.branch)

    def get_permissions(self):
        permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class AdminUserDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows detailed view  and update of admin_user
    """
    serializer_class = AdminUserSerializer

    def get_permissions(self):
        permission_classes = [IsMasterAdmin]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return AdminUser.objects.filter(branch__organization=self.request.user.adminuser.branch.organization)
        return AdminUser.objects.filter(branch=self.request.user.branch)
