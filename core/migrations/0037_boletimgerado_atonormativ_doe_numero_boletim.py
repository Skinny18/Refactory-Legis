# Generated by Django 4.1.3 on 2023-07-26 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_alter_atonormativ_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoletimGerado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('portarias_fks', models.CharField(default='', max_length=1000)),
                ('titulo', models.CharField(max_length=100)),
                ('conteudo_pdf', models.CharField(default='', max_length=100000)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='atonormativ',
            name='doe_numero_boletim',
            field=models.PositiveIntegerField(null=True, verbose_name='Número do Diário Oficial'),
        ),
    ]
