# Generated by Django 4.1.3 on 2023-08-16 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0083_atonormativ_criador'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atonormativ',
            name='criador',
        ),
        migrations.AddField(
            model_name='atonormativ',
            name='setor',
            field=models.CharField(max_length=50, null=True),
        ),
    ]