# Generated by Django 5.1.6 on 2025-04-10 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_remove_ranksm_project_ranksm_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewm',
            name='owner',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reviewm',
            name='value',
            field=models.CharField(choices=[('up', '👍'), ('down', '👎')], max_length=255),
        ),
    ]
