# Generated by Django 4.2.4 on 2023-08-10 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0071_remove_atonormativ_usr_cadastro_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atonormativ',
            name='data',
        ),
    ]