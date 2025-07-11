# Generated by Django 5.2 on 2025-04-12 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0003_alter_settings_fine_for_lost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='fine_for_lost',
            field=models.DecimalField(decimal_places=2, default=1000, max_digits=5),
        ),
        migrations.AlterField(
            model_name='settings',
            name='fine_per_lateday',
            field=models.DecimalField(decimal_places=2, default=1000, max_digits=5),
        ),
    ]
