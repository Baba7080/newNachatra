# Generated by Django 4.2.4 on 2023-09-19 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0010_alter_order_amount_alter_order_amount_due'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
