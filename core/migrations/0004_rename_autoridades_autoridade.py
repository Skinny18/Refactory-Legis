# Generated by Django 4.1.3 on 2023-01-27 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_autoridades_delete_task'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Autoridades',
            new_name='Autoridade',
        ),
    ]
