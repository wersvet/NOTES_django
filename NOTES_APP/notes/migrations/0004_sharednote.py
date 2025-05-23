# Generated by Django 5.2 on 2025-04-06 16:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_notes_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SharedNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shared_at', models.DateTimeField(auto_now_add=True)),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_with', to='notes.notes')),
                ('shared_with', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_notes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('note', 'shared_with')},
            },
        ),
    ]
