# Generated by Django 5.2 on 2025-04-12 09:22

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('max_loan_day', models.PositiveSmallIntegerField(default=7)),
                ('fine_per_lateday', models.DecimalField(decimal_places=2, default=2000, max_digits=5)),
                ('fine_for_lost', models.DecimalField(decimal_places=2, default=100000, max_digits=4)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
