# Generated by Django 4.2.4 on 2023-08-08 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0056_alter_atonormativ_setor_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atonormativ',
            name='setor_usuario',
            field=models.CharField(max_length=100, null=True, verbose_name='Setor do Usuário'),
        ),
    ]
