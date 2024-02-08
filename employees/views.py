from django.shortcuts import render, redirect
from employees.models import Employee, AdminUser, Education, WorkHistory,\
      Performance, BankDetails, EmployeeDocs, Payroll, Appointments, Attendance, Leave


def home(request):
    """WorkForceHub HOMEPAGE"""
    return render(request, 'base/base.html')