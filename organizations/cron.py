from django_cron import CronJobBase, Schedule
from .models import Branch, Organization

class ResetMonthlyCreatedEmployees(CronJobBase):
    RUN_AT_TIMES = ['00:00']  # Run at midnight

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'branch.reset_monthly_created_employees'
    def do(self):
        # Logic to reset the monthly_created_employees field
        Branch.objects.all().update(monthly_created_employees=0)
        Organization.objects.all().update(monthly_created_employees=0)