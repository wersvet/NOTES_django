# Generated by Django 5.2 on 2025-04-05 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notes',
            name='updated_at',
        ),
    ]
