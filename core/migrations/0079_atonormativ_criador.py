# Generated by Django 4.1.3 on 2023-08-16 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0078_remove_atonormativ_criador'),
    ]

    operations = [
        migrations.AddField(
            model_name='atonormativ',
            name='criador',
            field=models.CharField(default='user', max_length=45, verbose_name='Criador'),
        ),
    ]
