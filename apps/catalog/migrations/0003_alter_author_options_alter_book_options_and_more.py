# Generated by Django 5.2 on 2025-06-02 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_book_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['-updated_at']},
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['-updated_at']},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-updated_at']},
        ),
        migrations.AlterModelOptions(
            name='publisher',
            options={'ordering': ['-updated_at']},
        ),
        migrations.AlterModelOptions(
            name='shelf',
            options={'ordering': ['-updated_at']},
        ),
        migrations.AlterField(
            model_name='author',
            name='fullname',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='shelf',
            name='code',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
