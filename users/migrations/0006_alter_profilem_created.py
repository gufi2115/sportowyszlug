# Generated by Django 5.1.6 on 2025-04-14 15:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_profilem_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilem',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2025, 4, 14, 15, 31, 37, 429925, tzinfo=datetime.timezone.utc)),
        ),
    ]
