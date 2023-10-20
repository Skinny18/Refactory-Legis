# Generated by Django 4.1.3 on 2023-03-27 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_alter_atonormativ_ano_alter_atonormativ_data_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atonormativ',
            name='fformat_arq_edit',
        ),
        migrations.RemoveField(
            model_name='atonormativ',
            name='fformat_arq_pub',
        ),
        migrations.AlterField(
            model_name='composicao',
            name='boletim',
            field=models.CharField(max_length=1, verbose_name='caso seja uma boletim'),
        ),
        migrations.AlterField(
            model_name='composicao',
            name='portaria',
            field=models.CharField(max_length=1, verbose_name='caso seja uma portaria'),
        ),
        migrations.AlterField(
            model_name='composicao',
            name='resolucao',
            field=models.CharField(max_length=1, verbose_name='caso seja uma resolucao'),
        ),
    ]