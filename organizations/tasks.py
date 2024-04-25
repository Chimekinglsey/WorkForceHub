from celery import shared_task
from .models import Branch, Organization

@shared_task
def reset_monthly_created_employees():
    # Logic to reset the monthly_created_employees field
    Branch.objects.all().update(monthly_created_employees=0)
    Organization.objects.all().update(monthly_created_employees=0)
