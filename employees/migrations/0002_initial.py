# Generated by Django 5.0.1 on 2024-02-24 20:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('employees', '0001_initial'),
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminuser',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin_user', to='organizations.branch'),
        ),
        migrations.AddField(
            model_name='adminuser',
            name='delegated_branches',
            field=models.ManyToManyField(related_name='authorized_delegates', to='organizations.branch'),
        ),
        migrations.AddField(
            model_name='adminuser',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='admin_user_groups', to='auth.group'),
        ),
        migrations.AddField(
            model_name='adminuser',
            name='supervised_employees',
            field=models.ManyToManyField(blank=True, to='employees.adminuser'),
        ),
        migrations.AddField(
            model_name='adminuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='admin_user_permissions', to='auth.permission'),
        ),
        migrations.AddField(
            model_name='appointments',
            name='appointment_approval',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_appointments', to='employees.adminuser'),
        ),
        migrations.AddField(
            model_name='appointments',
            name='appointment_rejection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rejected_appointments', to='employees.adminuser'),
        ),
        migrations.AddField(
            model_name='employee',
            name='adminuser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='managed_employees', to='employees.adminuser'),
        ),
        migrations.AddField(
            model_name='employee',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='organizations.branch'),
        ),
        migrations.AddField(
            model_name='employee',
            name='supervised_employees',
            field=models.ManyToManyField(blank=True, to='employees.employee'),
        ),
        migrations.AddField(
            model_name='education',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='education', to='employees.employee'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='employees.employee'),
        ),
        migrations.AddField(
            model_name='appointments',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='employees.employee'),
        ),
        migrations.AddField(
            model_name='employeedocs',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='employees.employee'),
        ),
        migrations.AddField(
            model_name='leave',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leaves', to='employees.employee'),
        ),
        migrations.AddField(
            model_name='leave',
            name='leave_approval',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_leaves', to='employees.adminuser'),
        ),
        migrations.AddField(
            model_name='leave',
            name='leave_rejection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rejected_leaves', to='employees.adminuser'),
        ),
        migrations.AddField(
            model_name='passwordresettoken',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='employees.adminuser'),
        ),
        migrations.AddField(
            model_name='payroll',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payrolls', to='employees.employee'),
        ),
        migrations.AddField(
            model_name='performance',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performances', to='employees.employee'),
        ),
        migrations.AddField(
            model_name='training',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trainings', to='employees.employee'),
        ),
        migrations.AddField(
            model_name='workhistory',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='work_history', to='organizations.branch'),
        ),
        migrations.AddField(
            model_name='workhistory',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work_history', to='employees.employee'),
        ),
    ]
