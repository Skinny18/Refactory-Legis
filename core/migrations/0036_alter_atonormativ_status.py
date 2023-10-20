# Generated by Django 4.1.3 on 2023-07-04 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_atonormativ_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atonormativ',
            name='status',
            field=models.CharField(choices=[('revisao', 'Revisão'), ('aprovado', 'Aprovado'), ('pendente', 'Pendente'), ('cancelado', 'Cancelado')], default='revisao', max_length=10),
        ),
    ]