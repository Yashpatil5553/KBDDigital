# Generated by Django 5.2 on 2025-05-01 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0003_remove_userdata_income_total_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='RPM_Total',
        ),
    ]
