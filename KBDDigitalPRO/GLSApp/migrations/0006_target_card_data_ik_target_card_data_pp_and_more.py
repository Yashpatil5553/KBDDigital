# Generated by Django 5.2 on 2025-05-02 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GLSApp', '0005_target_card_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='target_card_data',
            name='IK',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='target_card_data',
            name='PP',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='target_card_data',
            name='SGA',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
