# Generated by Django 5.1.5 on 2025-02-08 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0006_alter_opdqueue_options_opdqueue_priority_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='duration',
            field=models.IntegerField(default=15),
        ),
    ]
