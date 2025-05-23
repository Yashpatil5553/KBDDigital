# Generated by Django 5.2 on 2025-05-18 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GLSApp', '0014_target_card_data_target_team1'),
    ]

    operations = [
        migrations.AddField(
            model_name='target_card_data',
            name='Target_KV',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='target_card_data',
            name='HP_Target',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='target_card_data',
            name='HR_Target',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='target_card_data',
            name='PB_Target',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='target_card_data',
            name='RJ_Target',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='target_card_data',
            name='TEL_Target',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='target_card_data',
            name='TURPHH_Target',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='target_card_data',
            name='Target_AD',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='target_card_data',
            name='Target_DTR',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='target_card_data',
            name='Target_Income',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='target_card_data',
            name='Target_NGL',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='target_card_data',
            name='Target_NID',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='target_card_data',
            name='Target_OBS',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='target_card_data',
            name='Target_RPM',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='target_card_data',
            name='Target_Sales',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='target_card_data',
            name='Target_Team',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='target_card_data',
            name='Target_Team1',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='target_card_data',
            name='Target_VV',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='target_card_data',
            name='UP_Target',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
