# Generated by Django 5.0.1 on 2024-04-25 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0006_alter_adminuser_employee_id_and_more'),
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'ordering': ['last_name', 'first_name'], 'verbose_name': 'Employee', 'verbose_name_plural': 'Employees'},
        ),
        migrations.AddField(
            model_name='adminuser',
            name='delegated_branches',
            field=models.ManyToManyField(related_name='authorized_delegates', to='organizations.branch'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='designation',
            field=models.CharField(choices=[('--Select--', '--Select--'), ('Employee', 'Employee'), ('Intern', 'Intern'), ('Trainee', 'Trainee'), ('Associate', 'Associate'), ('Assistant', 'Assistant'), ('Officer', 'Officer'), ('Analyst', 'Analyst'), ('Coordinator', 'Coordinator'), ('Specialist', 'Specialist'), ('Consultant', 'Consultant'), ('Advisor', 'Advisor'), ('Supervisor', 'Supervisor'), ('Manager', 'Manager'), ('Director', 'Director'), ('Executive', 'Executive'), ('President', 'President'), ('CEO', 'CEO'), ('CFO', 'CFO'), ('CTO', 'CTO'), ('CIO', 'CIO'), ('COO', 'COO'), ('Chairman', 'Chairman'), ('Board Member', 'Board Member'), ('Other', 'Other')], default='Employee', max_length=30, verbose_name='Designation'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='emergency_contacts',
            field=models.TextField(null=True, verbose_name='Emergency contacts'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='employment_status',
            field=models.CharField(choices=[('--Select--', '--Select--'), ('Active', 'Active'), ('Inactive', 'Inactive'), ('Suspended', 'Suspended'), ('Terminated', 'Terminated'), ('Resigned', 'Resigned'), ('Retired', 'Retired'), ('Deceased', 'Deceased'), ('On Leave', 'On Leave'), ('On Training', 'On Training'), ('On Probation', 'On Probation'), ('Other', 'Other')], default='Active', max_length=20, verbose_name='Employment status'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='employment_type',
            field=models.CharField(choices=[('--Select--', '--Select--'), ('Full-time', 'Full-time'), ('Part-time', 'Part-time'), ('Contract', 'Contract'), ('Intern', 'Intern'), ('Volunteer', 'Volunteer'), ('Temporary', 'Temporary'), ('Seasonal', 'Seasonal'), ('Freelance', 'Freelance'), ('Remote', 'Remote'), ('Disabled', 'Disabled'), ('Other', 'Other')], max_length=100, verbose_name='Employment type'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='gender',
            field=models.CharField(blank=True, choices=[('--Select--', '--Select--'), ('Male', 'Male'), ('Female', 'Female')], max_length=10, null=True, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='highest_qualification',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Highest qualification'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='level',
            field=models.CharField(blank=True, choices=[('--Select--', '--Select--'), ('Entry-level', 'Entry-level'), ('Mid-level', 'Mid-level'), ('Senior-level', 'Senior-level'), ('Executive', 'Executive'), ('Top-level', 'Top-level'), ('Other', 'Other')], max_length=30, null=True, verbose_name='Level'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='marital_status',
            field=models.CharField(blank=True, choices=[('--Select--', '--Select--'), ('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed'), ('Separated', 'Separated'), ('Other', 'Other')], max_length=15, null=True, verbose_name='Marital status'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='nationality',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Nationality'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='next_of_kin_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Next of kin name'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='next_of_kin_phone_number',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Next of kin phone number'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Phone number'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='state_of_origin',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='State of origin'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='designation',
            field=models.CharField(choices=[('--Select--', '--Select--'), ('Employee', 'Employee'), ('Intern', 'Intern'), ('Trainee', 'Trainee'), ('Associate', 'Associate'), ('Assistant', 'Assistant'), ('Officer', 'Officer'), ('Analyst', 'Analyst'), ('Coordinator', 'Coordinator'), ('Specialist', 'Specialist'), ('Consultant', 'Consultant'), ('Advisor', 'Advisor'), ('Supervisor', 'Supervisor'), ('Manager', 'Manager'), ('Director', 'Director'), ('Executive', 'Executive'), ('President', 'President'), ('CEO', 'CEO'), ('CFO', 'CFO'), ('CTO', 'CTO'), ('CIO', 'CIO'), ('COO', 'COO'), ('Chairman', 'Chairman'), ('Board Member', 'Board Member'), ('Other', 'Other')], default='Employee', max_length=30, verbose_name='Designation'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(blank=True, max_length=254, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='emergency_contacts',
            field=models.TextField(null=True, verbose_name='Emergency contacts'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='employment_status',
            field=models.CharField(choices=[('--Select--', '--Select--'), ('Active', 'Active'), ('Inactive', 'Inactive'), ('Suspended', 'Suspended'), ('Terminated', 'Terminated'), ('Resigned', 'Resigned'), ('Retired', 'Retired'), ('Deceased', 'Deceased'), ('On Leave', 'On Leave'), ('On Training', 'On Training'), ('On Probation', 'On Probation'), ('Other', 'Other')], default='Active', max_length=20, verbose_name='Employment status'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='employment_type',
            field=models.CharField(choices=[('--Select--', '--Select--'), ('Full-time', 'Full-time'), ('Part-time', 'Part-time'), ('Contract', 'Contract'), ('Intern', 'Intern'), ('Volunteer', 'Volunteer'), ('Temporary', 'Temporary'), ('Seasonal', 'Seasonal'), ('Freelance', 'Freelance'), ('Remote', 'Remote'), ('Disabled', 'Disabled'), ('Other', 'Other')], max_length=100, verbose_name='Employment type'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='First name'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.CharField(blank=True, choices=[('--Select--', '--Select--'), ('Male', 'Male'), ('Female', 'Female')], max_length=10, null=True, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='highest_qualification',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Highest qualification'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='Last name'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='level',
            field=models.CharField(blank=True, choices=[('--Select--', '--Select--'), ('Entry-level', 'Entry-level'), ('Mid-level', 'Mid-level'), ('Senior-level', 'Senior-level'), ('Executive', 'Executive'), ('Top-level', 'Top-level'), ('Other', 'Other')], max_length=30, null=True, verbose_name='Level'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='marital_status',
            field=models.CharField(blank=True, choices=[('--Select--', '--Select--'), ('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed'), ('Separated', 'Separated'), ('Other', 'Other')], max_length=15, null=True, verbose_name='Marital status'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='nationality',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Nationality'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='next_of_kin_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Next of kin name'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='next_of_kin_phone_number',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Next of kin phone number'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Phone number'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='state_of_origin',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='State of origin'),
        ),
        migrations.AlterField(
            model_name='finance',
            name='asset_turnover_ratio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Asset Turnover Ratio'),
        ),
        migrations.AlterField(
            model_name='finance',
            name='budget_variance',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Budget Variance'),
        ),
        migrations.AlterField(
            model_name='finance',
            name='budgeted_expenses',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Budgeted Expenses'),
        ),
        migrations.AlterField(
            model_name='finance',
            name='budgeted_revenue',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Budgeted Revenue'),
        ),
        migrations.AlterField(
            model_name='finance',
            name='current_ratio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Current Ratio'),
        ),
        migrations.AlterField(
            model_name='finance',
            name='debt_to_equity_ratio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Debt-to-Equity Ratio'),
        ),
        migrations.AlterField(
            model_name='finance',
            name='ebitda',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='EBITDA'),
        ),
        migrations.AlterField(
            model_name='finance',
            name='forecasted_expenses',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Forecasted Expenses'),
        ),
        migrations.AlterField(
            model_name='finance',
            name='forecasted_revenue',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Forecasted Revenue'),
        ),
        migrations.AlterField(
            model_name='finance',
            name='gross_profit',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Gross Profit'),
        ),
        migrations.AlterField(
            model_name='finance',
            name='interest_coverage_ratio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Interest Coverage Ratio'),
        ),
        migrations.AlterField(
            model_name='finance',
            name='interest_expenses',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Interest Expenses'),
        ),
        migrations.AlterField(
            model_name='finance',
            name='inventory_turnover_ratio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Inventory Turnover Ratio'),
        ),
        migrations.AlterField(
            model_name='finance',
            name='net_profit',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Net Profit'),
        ),
        migrations.AlterField(
            model_name='finance',
            name='operating_expenses',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Operating Expenses'),
        ),
        migrations.AlterField(
            model_name='finance',
            name='operating_profit',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Operating Profit'),
        ),
        migrations.AlterField(
            model_name='finance',
            name='profit_margin',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Profit Margin (%)'),
        ),
        migrations.AlterField(
            model_name='finance',
            name='quick_ratio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Quick Ratio'),
        ),
        migrations.AlterField(
            model_name='finance',
            name='return_on_assets',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Return on Assets (%)'),
        ),
        migrations.AlterField(
            model_name='finance',
            name='return_on_equity',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Return on Equity (%)'),
        ),
        migrations.AlterField(
            model_name='finance',
            name='taxes',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Taxes'),
        ),
        migrations.AlterField(
            model_name='finance',
            name='total_expenses',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Total Expenses'),
        ),
        migrations.AlterField(
            model_name='finance',
            name='total_revenue',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Total Revenue'),
        ),
    ]
