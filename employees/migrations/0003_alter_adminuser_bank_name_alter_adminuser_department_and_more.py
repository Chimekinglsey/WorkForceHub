# Generated by Django 5.0.1 on 2024-04-25 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminuser',
            name='bank_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='bank name'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='department',
            field=models.CharField(max_length=150, verbose_name='Department/division'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='designation',
            field=models.CharField(choices=[('--Select--', '--Select--'), ('Employee', 'Employee'), ('Intern', 'Intern'), ('Trainee', 'Trainee'), ('Associate', 'Associate'), ('Assistant', 'Assistant'), ('Officer', 'Officer'), ('Analyst', 'Analyst'), ('Coordinator', 'Coordinator'), ('Specialist', 'Specialist'), ('Consultant', 'Consultant'), ('Advisor', 'Advisor'), ('Supervisor', 'Supervisor'), ('Manager', 'Manager'), ('Director', 'Director'), ('Executive', 'Executive'), ('President', 'President'), ('CEO', 'CEO'), ('CFO', 'CFO'), ('CTO', 'CTO'), ('CIO', 'CIO'), ('COO', 'COO'), ('Chairman', 'Chairman'), ('Board Member', 'Board Member'), ('Other', 'Other')], default='Employee', max_length=100, verbose_name='Designation'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='employee_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Employee ID'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='job_role',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Job role'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='level',
            field=models.CharField(blank=True, choices=[('--Select--', '--Select--'), ('Entry-level', 'Entry-level'), ('Mid-level', 'Mid-level'), ('Senior-level', 'Senior-level'), ('Executive', 'Executive'), ('Top-level', 'Top-level'), ('Other', 'Other')], max_length=50, null=True, verbose_name='Level'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='middle_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Middle name'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='nationality',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Nationality'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='next_of_kin_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Next of kin name'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone number'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='state_of_origin',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='State of origin'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='bank_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='bank name'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='department',
            field=models.CharField(max_length=150, verbose_name='Department/division'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='designation',
            field=models.CharField(choices=[('--Select--', '--Select--'), ('Employee', 'Employee'), ('Intern', 'Intern'), ('Trainee', 'Trainee'), ('Associate', 'Associate'), ('Assistant', 'Assistant'), ('Officer', 'Officer'), ('Analyst', 'Analyst'), ('Coordinator', 'Coordinator'), ('Specialist', 'Specialist'), ('Consultant', 'Consultant'), ('Advisor', 'Advisor'), ('Supervisor', 'Supervisor'), ('Manager', 'Manager'), ('Director', 'Director'), ('Executive', 'Executive'), ('President', 'President'), ('CEO', 'CEO'), ('CFO', 'CFO'), ('CTO', 'CTO'), ('CIO', 'CIO'), ('COO', 'COO'), ('Chairman', 'Chairman'), ('Board Member', 'Board Member'), ('Other', 'Other')], default='Employee', max_length=100, verbose_name='Designation'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='employee_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Employee ID'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='job_role',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Job role'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='level',
            field=models.CharField(blank=True, choices=[('--Select--', '--Select--'), ('Entry-level', 'Entry-level'), ('Mid-level', 'Mid-level'), ('Senior-level', 'Senior-level'), ('Executive', 'Executive'), ('Top-level', 'Top-level'), ('Other', 'Other')], max_length=50, null=True, verbose_name='Level'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='middle_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Middle name'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='nationality',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Nationality'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='next_of_kin_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Next of kin name'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone number'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='state_of_origin',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='State of origin'),
        ),
    ]
