# Generated by Django 4.1.3 on 2023-08-16 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0079_atonormativ_criador'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atonormativ',
            name='criador',
        ),
    ]