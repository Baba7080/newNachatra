# Generated by Django 4.2.4 on 2023-09-19 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0011_profile_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='mail',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
