# Generated by Django 5.2 on 2025-04-18 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_member_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='nis',
            field=models.CharField(blank=True, max_length=13, null=True, unique=True),
        ),
    ]
