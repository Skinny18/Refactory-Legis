# Generated by Django 4.1.3 on 2023-03-27 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_remove_atonormativ_fformat_arq_edit_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Autoridade',
        ),
        migrations.DeleteModel(
            name='Editor',
        ),
    ]
