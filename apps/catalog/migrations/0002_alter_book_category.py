# Generated by Django 5.2 on 2025-05-27 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='related_books', to='catalog.category'),
        ),
    ]
