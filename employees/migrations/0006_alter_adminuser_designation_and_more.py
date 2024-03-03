# Generated by Django 5.0.1 on 2024-03-01 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0005_alter_passwordresettoken_token_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminuser',
            name='designation',
            field=models.CharField(choices=[('--Select--', '--Select--'), ('Employee', 'Employee'), ('Intern', 'Intern'), ('Trainee', 'Trainee'), ('Associate', 'Associate'), ('Assistant', 'Assistant'), ('Officer', 'Officer'), ('Analyst', 'Analyst'), ('Coordinator', 'Coordinator'), ('Specialist', 'Specialist'), ('Consultant', 'Consultant'), ('Advisor', 'Advisor'), ('Supervisor', 'Supervisor'), ('Manager', 'Manager'), ('Director', 'Director'), ('Executive', 'Executive'), ('President', 'President'), ('CEO', 'CEO'), ('CFO', 'CFO'), ('CTO', 'CTO'), ('CIO', 'CIO'), ('COO', 'COO'), ('Chairman', 'Chairman'), ('Board Member', 'Board Member'), ('Other', 'Other')], default='Employee', max_length=30, verbose_name='Designation'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='employment_status',
            field=models.CharField(choices=[('--Select--', '--Select--'), ('Active', 'Active'), ('Inactive', 'Inactive'), ('Suspended', 'Suspended'), ('Terminated', 'Terminated'), ('Resigned', 'Resigned'), ('Retired', 'Retired'), ('Deceased', 'Deceased'), ('On Leave', 'On Leave'), ('On Training', 'On Training'), ('On Probation', 'On Probation'), ('Other', 'Other')], default='Active', max_length=20, verbose_name='Employment status'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='joining_date',
            field=models.DateField(blank=True, default='1600-01-01', null=True, verbose_name='Joining date'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='designation',
            field=models.CharField(choices=[('--Select--', '--Select--'), ('Employee', 'Employee'), ('Intern', 'Intern'), ('Trainee', 'Trainee'), ('Associate', 'Associate'), ('Assistant', 'Assistant'), ('Officer', 'Officer'), ('Analyst', 'Analyst'), ('Coordinator', 'Coordinator'), ('Specialist', 'Specialist'), ('Consultant', 'Consultant'), ('Advisor', 'Advisor'), ('Supervisor', 'Supervisor'), ('Manager', 'Manager'), ('Director', 'Director'), ('Executive', 'Executive'), ('President', 'President'), ('CEO', 'CEO'), ('CFO', 'CFO'), ('CTO', 'CTO'), ('CIO', 'CIO'), ('COO', 'COO'), ('Chairman', 'Chairman'), ('Board Member', 'Board Member'), ('Other', 'Other')], default='Employee', max_length=30, verbose_name='Designation'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='employment_status',
            field=models.CharField(choices=[('--Select--', '--Select--'), ('Active', 'Active'), ('Inactive', 'Inactive'), ('Suspended', 'Suspended'), ('Terminated', 'Terminated'), ('Resigned', 'Resigned'), ('Retired', 'Retired'), ('Deceased', 'Deceased'), ('On Leave', 'On Leave'), ('On Training', 'On Training'), ('On Probation', 'On Probation'), ('Other', 'Other')], default='Active', max_length=20, verbose_name='Employment status'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='joining_date',
            field=models.DateField(blank=True, default='1600-01-01', null=True, verbose_name='Joining date'),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='month',
            field=models.CharField(default='March', max_length=20, verbose_name='month'),
        ),
    ]
