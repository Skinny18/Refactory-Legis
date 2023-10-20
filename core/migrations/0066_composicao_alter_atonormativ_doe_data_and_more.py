# Generated by Django 4.2.4 on 2023-08-08 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0065_alter_atonormativ_doe_data_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Composicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usario', models.CharField(max_length=80, verbose_name='Usuario')),
                ('sigla_setor', models.CharField(max_length=20, verbose_name='sigla do setor')),
                ('nome_setor', models.CharField(max_length=80, verbose_name='nome do setor')),
            ],
        ),
        migrations.AlterField(
            model_name='atonormativ',
            name='doe_data',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data do Diário Oficial'),
        ),
        migrations.AlterField(
            model_name='atonormativ',
            name='doe_pagina',
            field=models.CharField(max_length=40, verbose_name='Página do Diário Oficial'),
        ),
        migrations.AlterField(
            model_name='atonormativ',
            name='doe_secao',
            field=models.CharField(max_length=40, verbose_name='Seção do Diário Oficial'),
        ),
    ]
