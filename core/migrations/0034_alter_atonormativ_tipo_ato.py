# Generated by Django 4.1.3 on 2023-03-31 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_atonormativ_tipo_ato'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atonormativ',
            name='tipo_ato',
            field=models.CharField(max_length=45, null=True, verbose_name='ato'),
        ),
    ]
