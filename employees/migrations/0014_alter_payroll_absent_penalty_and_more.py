# Generated by Django 5.0.1 on 2024-02-20 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0013_alter_payroll_other_allowance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payroll',
            name='absent_penalty',
            field=models.IntegerField(default=0, verbose_name='absence penalty'),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='late_penalty',
            field=models.IntegerField(default=0, verbose_name='lateness penalty'),
        ),
    ]
