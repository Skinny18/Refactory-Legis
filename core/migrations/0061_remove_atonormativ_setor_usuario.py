# Generated by Django 4.2.4 on 2023-08-08 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0060_alter_atonormativ_setor_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atonormativ',
            name='setor_usuario',
        ),
    ]