# Generated by Django 5.1 on 2024-08-24 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='tax',
            new_name='fee',
        ),
    ]
