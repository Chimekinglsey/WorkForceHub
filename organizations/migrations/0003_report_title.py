# Generated by Django 5.0.1 on 2024-02-25 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='title',
            field=models.CharField(default='Old records', max_length=250, verbose_name='Title'),
            preserve_default=False,
        ),
    ]
