# Generated by Django 4.1.3 on 2023-09-06 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0093_atohash'),
    ]

    operations = [
        migrations.AddField(
            model_name='atohash',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='pdfs/'),
        ),
    ]
