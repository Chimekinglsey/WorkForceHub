# Generated by Django 5.0.1 on 2024-02-12 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminuser',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
    ]
