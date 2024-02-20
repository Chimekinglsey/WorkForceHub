# Generated by Django 5.0.1 on 2024-02-19 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0011_alter_payroll_month'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminuser',
            name='basic_salary',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='Salary'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='basic_salary',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='Salary'),
        ),
    ]
