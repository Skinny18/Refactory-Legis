# Generated by Django 4.1.3 on 2023-03-31 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_alter_atonormativ_assinante1'),
    ]

    operations = [
        migrations.CreateModel(
            name='Composicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usario', models.CharField(max_length=80, verbose_name='Usuario')),
                ('sigla_setor', models.CharField(max_length=20, verbose_name='sigla do setor')),
                ('nome_setor', models.CharField(max_length=80, verbose_name='nome do setor')),
                ('tipo_ato', models.CharField(choices=[('portaria', 'Portaria'), ('resolucao', 'Resolução'), ('boletim', 'Boletim')], max_length=10, verbose_name='Tipo de Ato Normativo')),
            ],
        ),
    ]