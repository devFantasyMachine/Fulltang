# Generated by Django 3.2.9 on 2023-01-12 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polyclinic', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='freeBeds',
            new_name='busyBeds',
        ),
    ]
