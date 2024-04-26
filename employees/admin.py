from django.contrib import admin
from .models import Employee, Education, EmployeeDocs, WorkHistory, Performance, Appointments, Leave, Attendance, Payroll, Training, AdminUser, Finance

models = [Employee, Education, EmployeeDocs, Performance, Appointments, 
          Leave, Attendance, Payroll, Training, AdminUser, WorkHistory, Finance]
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('username', 'last_name', 'email', 'phone', 'designation')
    list_filter = ('username', 'last_name', 'email', 'phone', 'designation')
    search_fields = ('username', 'last_name', 'email', 'phone', 'designation')

class EducationAdmin(admin.ModelAdmin):
    """List display for employee education"""
    list_display = ('employee', 'course', 'institution', 'start_date', 'end_date')

for model in models:
    admin.site.register(model)
