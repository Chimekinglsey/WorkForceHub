# Generated by Django 5.0.1 on 2024-02-27 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_finance'),
    ]

    operations = [
        migrations.RenameField(
            model_name='finance',
            old_name='owner',
            new_name='created_by',
        ),
    ]
