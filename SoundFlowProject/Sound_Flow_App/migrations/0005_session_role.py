# Generated by Django 5.1.1 on 2024-10-08 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sound_Flow_App', '0004_session_supported_engineers'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='role',
            field=models.CharField(blank=True, choices=[('created_by', 'Engineer'), ('supported_engineers', 'Supported_engineers')], max_length=20, null=True),
        ),
    ]
