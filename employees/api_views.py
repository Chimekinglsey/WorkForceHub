from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, generics, permissions
from .serializers import EmployeeSerializer, AdminUserSerializer
from .models import Employee, AdminUser
from .permissions import IsAdminUser

def home(request):
    return HttpResponse("Welcome to WorkforceHub")

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows employees to be viewed or edited.
    """
    queryset = Employee.objects.all().order_by('created_at')
    serializer_class = EmployeeSerializer

class EmployeeDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    """ API endpoint that allows detailed view and update of employee"""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminUser]

class AdminUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin users to be viewed or edited.
    """
    queryset = AdminUser.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, permissions.IsAdminUser]
class AdminUserDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows detailed view  and update of admin_user
    """
    queryset = AdminUser.objects.all()
    serializer_class = AdminUserSerializer