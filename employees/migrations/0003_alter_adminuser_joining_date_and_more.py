# Generated by Django 5.0.1 on 2024-03-07 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminuser',
            name='joining_date',
            field=models.DateField(blank=True, null=True, verbose_name='Joining date'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='joining_date',
            field=models.DateField(blank=True, null=True, verbose_name='Joining date'),
        ),
    ]