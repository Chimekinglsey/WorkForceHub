from django.contrib import admin
from .models import Organization, OrgDocuments, Branch

admin.site.register(Organization)
admin.site.register(OrgDocuments)
admin.site.register(Branch)
# Register your models here.
