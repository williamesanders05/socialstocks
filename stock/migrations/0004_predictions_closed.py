# Generated by Django 3.2 on 2021-07-01 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_predictions_timeposted'),
    ]

    operations = [
        migrations.AddField(
            model_name='predictions',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]