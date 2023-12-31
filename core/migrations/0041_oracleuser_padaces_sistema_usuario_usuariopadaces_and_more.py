# Generated by Django 4.1.3 on 2023-08-02 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_alter_atonormativ_autoridade1'),
    ]

    operations = [
        migrations.CreateModel(
            name='OracleUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('USER_LDAP', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'OBERON.USUARIO',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Padaces',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PADACES', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'OBERON.PADACES',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sistema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SISTEMA', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'OBERON.SISTEMA',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('USER_LDAP', models.CharField(max_length=100)),
                ('ATIVO', models.CharField(max_length=1)),
            ],
            options={
                'db_table': 'OBERON.USUARIO',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Usuariopadaces',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'OBERON.USUARIOPADACES',
                'managed': False,
            },
        ),
        migrations.AddField(
            model_name='atonormativ',
            name='criador',
            field=models.CharField(default='user', max_length=45, verbose_name='Criador'),
        ),
        migrations.AddField(
            model_name='atonormativ',
            name='pendestes_texto',
            field=models.TextField(default='Sem pendencias', max_length=1000, null=True, verbose_name='Texto pendentes'),
        ),
    ]
