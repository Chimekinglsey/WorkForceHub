# Generated by Django 5.0.1 on 2024-02-19 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0010_alter_payroll_month'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payroll',
            name='month',
            field=models.CharField(default='February', max_length=20, verbose_name='month'),
        ),
    ]
