# Generated by Django 4.2.4 on 2023-08-08 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0045_alter_atonormativ_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atonormativ',
            name='get_setor',
        ),
        migrations.AlterModelTable(
            name='atonormativ',
            table=None,
        ),
    ]
