# Generated by Django 5.2 on 2025-05-02 04:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GLSApp', '0001_initial'),
        ('homeapp', '0004_remove_userdata_rpm_total'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Target_Data',
            new_name='Target_Data_IST',
        ),
    ]
