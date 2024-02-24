from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver



class Organization(models.Model):
    """Model for organization"""
    INDUSTRY_CHOICES = (
        ('Technology', _('Technology')),
        ('Healthcare', _('Healthcare')),
        ('Finance', _('Finance')),
        ('Manufacturing', _('Manufacturing')),
        ('Education', _('Education')),
        ('Retail', _('Retail')),
        ('Hospitality', _('Hospitality')),
        ('Other', _('Other'))
    )

    BRANCHES_CHOICES = (
        ('1 - 10', _('1 - 10')),
        ('10 - 50', _('10 - 50')),
        ('51 - 100', _('51 - 100')),
        ('101 - 500', _('101 - 500')),
        ('Above 500', _('Above 500'))
    )

    EMPLOYEES_CHOICES = (
        ('1 - 20', _('1 - 20')),
        ('21 - 100', _('21 - 100')),
        ('101 - 500', _('101 - 500')),
        ('501 - 1000', _('501 - 1000')),
        ('Above 1000', _('Above 1000'))
    )

    admin_user = models.ForeignKey('employees.AdminUser', on_delete=models.CASCADE, related_name='organizations')
    name = models.CharField(_('name'), max_length=250)
    org_id = models.CharField(_('organization id'), max_length=12, unique=True)
    industry = models.CharField(_('industry'), choices=INDUSTRY_CHOICES, max_length=100, blank=True)
    sector = models.CharField(_('sector'), max_length=200, blank=True)
    size = models.CharField(_('size'), choices=EMPLOYEES_CHOICES, default='1 - 20', max_length=100, blank=True)
    branches = models.CharField(_('branches'), choices=BRANCHES_CHOICES, default='1 - 10', max_length=100, blank=True)
    headquarter = models.CharField(_('headquarter'), max_length=250, null=True, blank=True)
    website = models.URLField(_('website'), max_length=250, null=True, blank=True)
    description = models.TextField(_('description'), null=True, blank=True)
    contact_phone = models.CharField(_('contact phone'), max_length=20, null=True, blank=True)
    contact_email = models.EmailField(_('contact email'), max_length=250, null=True, blank=True)
    mailing_address = models.CharField(_('mailing address'), max_length=250, null=True, blank=True)
    revenue = models.DecimalField(_('annual revenue'), max_digits=15, decimal_places=2, null=True, blank=True)
    profit = models.DecimalField(_('annual profit'), max_digits=15, decimal_places=2, null=True, blank=True)
    # financial_year_end = models.DateField(_('financial year end'), null=True, blank=True)
    employee_benefits = models.TextField(_('employee benefits'), null=True, blank=True)
    hierarchy = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subsidiaries')
    facebook = models.URLField(_('facebook'), max_length=250, null=True, blank=True)
    twitter = models.URLField(_('twitter'), max_length=250, null=True, blank=True)
    linkedin = models.URLField(_('linkedin'), max_length=250, null=True, blank=True)
    monthly_created_employees = models.PositiveIntegerField(_('monthly employees added'), default=0)
    certifications = models.TextField(_('certifications'), null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')
        ordering = ['name']

    @receiver(post_save, sender='employees.Employee')
    def increment_monthly_created_employees(sender, instance, created, **kwargs):
        if created:
            instance.branch.organization.monthly_created_employees += 1
            instance.branch.save()            


    def __str__(self):
        return self.name


class Branch(models.Model):
    """Model for branch"""
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization_branches')
    name = models.CharField(_('name'), max_length=100)
    branch_id = models.CharField(_('branch id'), max_length=5, unique=True)
    location = models.CharField(_('location'), max_length=250)
    email = models.EmailField(_('email'), max_length=250, null=True, blank=True)
    contact_phone = models.CharField(_('contact phone'), max_length=20, null=True, blank=True)
    contact_email = models.EmailField(_('contact email'), max_length=250, null=True, blank=True)
    facebook = models.URLField(_('facebook'), max_length=250, null=True, blank=True)
    twitter = models.URLField(_('twitter'), max_length=250, null=True, blank=True)
    linkedin = models.URLField(_('linkedin'), max_length=250, null=True, blank=True)
    description = models.TextField(_('description'), blank=True)
    monthly_created_employees = models.PositiveIntegerField(_('monthly employees added'), default=0)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('branch')
        verbose_name_plural = _('branches')
        ordering = ['name']


    # a function that increments the monthly_employee_added field by 1, saves the instance and resets to 0 at the end of the month
    @receiver(post_save, sender='employees.Employee')
    def increment_monthly_created_employees(sender, instance, created, **kwargs):
        if created:
            instance.branch.monthly_created_employees += 1
            instance.branch.save()            

    def __str__(self):
        return self.name
class OrgDocuments(models.Model):
    """Model for organization documents"""
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='documents')
    document_name = models.CharField(_('document name'), max_length=100)
    document = models.FileField(_('document'), upload_to='organizations/documents/')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')
        ordering = ['document_name', '-created_at']


class Transfer(models.Model):
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('approved', _('Approved')),
        ('declined', _('Declined')),
    )
    

    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='transfers')
    source_branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='outgoing_transfers')
    destination_branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='incoming_transfers')
    reason = models.TextField(_('Reason for Transfer'))
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='Pending')
    requested_by = models.ForeignKey('employees.AdminUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='requested_transfers')
    approved_by = models.ForeignKey('employees.AdminUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_transfers')
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Transfer')
        verbose_name_plural = _('Transfers')
