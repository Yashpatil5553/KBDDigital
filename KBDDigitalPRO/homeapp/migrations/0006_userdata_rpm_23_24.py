# Generated by Django 5.2 on 2025-05-02 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0005_userdata_hp_t_24_25_userdata_hr_t_24_25_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='RPM_23_24',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
