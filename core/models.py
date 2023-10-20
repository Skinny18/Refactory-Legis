from django.db import models
from tinymce.models import HTMLField
from django.utils import timezone
import datetime
from django.utils.html import strip_tags
from django.contrib.auth.models import User

import pytz


class Composicao(models.Model):
    # composicao_id = models.AutoField(primary_key=True)
    usario = models.CharField(max_length=80, verbose_name='Usuario')
    sigla_setor = models.CharField(max_length=20, verbose_name='sigla do setor')
    nome_setor = models.CharField(max_length=80, verbose_name='nome do setor')
    # portaria = models.CharField(max_length=1,verbose_name='caso seja uma portaria')
    # resolucao = models.CharField(max_length=1,verbose_name='caso seja uma resolucao')
    # boletim = models.CharField(max_length=1,verbose_name='caso seja uma boletim')
    db_table = 'Composicao'


# class Usario (models.Model):
#     usario = models.CharField(max_length=255,primary_key=True)

# class Emitente (models.Model):
#     sigla = models.CharField(max_length=255)
#     nome = models.CharField(max_length=255)

# class TipoLegislacao(models.Model):
#      tipo = models.CharField(max_length=40, verbose_name='Tipo de ato')

# class EmitenteTipoLeg(models.Model):
#     tipolegislacao = models.ForeignKey(TipoLegislacao,on_delete=models.CASCADE)
#     emitente = models.ForeignKey(Emitente,on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('tipolegislacao', 'emitente')

#     # class Meta:
#     #     primary_key = ('tipolegislacao', 'emitente')
#     #     verbose_name = 'Emitente-Tipo de Legislação'
#     #     verbose_name_plural = 'Emitentes-Tipos de Legislação'
#     #     unique_together = ('tipolegislacao', 'emitente')


class Autoridade(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nome}/{self.id}"


class AtoNormativ(models.Model):
    STATUS_CHOICES = [
        ('revisao', 'Revisão'),
        ('aprovado', 'Aprovado'),
        ('pendente', 'Pendente'),
        ('cancelado', 'Cancelado'),
    ]

    ATO_CHOICES = [
        ('portaria', 'Portaria'),
        ('resolucao', 'Resolucao'),
    ]
    # data = models.DateTimeField(default=timezone.datetime(2000, 10, 10, tzinfo=pytz.timezone('America/Manaus')),
    #                             verbose_name='Data de criação')
    numero = models.IntegerField(null=True, blank=True)
    # nao esquecer de que chave era unica abaixo
    ano = models.PositiveIntegerField(null=True, verbose_name='Ano')
    doe_data = models.DateTimeField(auto_now_add=True, verbose_name='Data do Diário Oficial')
    # doe_numero = models.PositiveIntegerField(null=True, verbose_name='Número do Diário Oficial')
    doe_numero_boletim = models.PositiveIntegerField(null=True, verbose_name='Número do Diário Oficial')
    # doe_secao = models.CharField(max_length=40,blank=False, verbose_name='Seção do Diário Oficial')
    # doe_pagina = models.CharField(max_length=40,null=True, verbose_name='Página do Diário Oficial')
    dt_cadastro = models.DateTimeField(null=True, verbose_name='Data de cadastro')
    # usr_cadastro = models.CharField(null=False, default='enzo', max_length=40, verbose_name='Usuário de cadastro')
    ementa = models.TextField(max_length=400, verbose_name='Ementa', null=False)
    texto_normativo = models.TextField(null=False, default='escrever', max_length=1000, verbose_name='Texto normativo')
    publicado = models.CharField(null=True, default='n', max_length=1, verbose_name='Publicado')
    dt_alteracao = models.DateField(auto_now=True, verbose_name='Data de alteração')
    usr_alteracao = models.CharField(max_length=20, verbose_name='Usuário de alteração')
    dt_publicado = models.DateField(null=True, blank=True, verbose_name='Data de publicação')
    usr_publicacao = models.CharField(max_length=45, verbose_name='Usuário de publicação')
    autoridade1 = models.CharField(max_length=45, null=False, default='setor', verbose_name='Autoridade 1')
    autoridade2 = models.CharField(max_length=45, null=True, default='setor', verbose_name='Autoridade 2')
    assinante1 = models.ForeignKey(Autoridade, on_delete=models.CASCADE, related_name='ato_normativ_assinante1',
                                   verbose_name='Assinante 1')
    assinante2 = models.ForeignKey(Autoridade, on_delete=models.CASCADE, null=True,
                                   related_name='ato_normativ_assinante2', verbose_name='Assinante 2')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='revisao')
    # tipo_ato = models.ForeignKey(Composicao, on_delete=models.CASCADE, verbose_name='Tipo de Ato Normativo',
    #                           limit_choices_to={'tipo_ato__in': [('portaria', 'Portaria'), ('resolucao', 'Resolução'), ('boletim', 'Boletim')]}, default=None)
    tipo_ato = models.CharField(max_length=45, null=True, verbose_name='ato')
    pendestes_texto = models.TextField(null=True, default='Sem pendencias', max_length=1000,
                                       verbose_name='Texto pendentes')
    criador = models.CharField(max_length=45, null=False, default='user', verbose_name='Criador')
    setores_uea = models.PositiveIntegerField(null=True)
    db_table = 'AtoNormativ'

    def __str__(self):
        return f"{self.texto_normativo}/{self.ementa}"

class BoletimGerado(models.Model):
    STATUS_CHOICES = [
        ('revisao', 'Revisão'),
        ('aprovado', 'Aprovado'),
    ]

    portarias_fks = models.CharField(max_length=1000, default='')
    titulo = models.CharField(max_length=100)
    conteudo_pdf = models.CharField(max_length=100000, default='')
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='revisao')
    setores_uea = models.ForeignKey(AtoNormativ, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.titulo


class OracleUser(models.Model):
    USER_LDAP = models.CharField(max_length=100)  # Ou o tipo de campo adequado para o campo USER_LDAP

    class Meta:
        managed = False
        db_table = 'OBERON.USUARIO'


class Usuario(models.Model):
    USER_LDAP = models.CharField(max_length=100)
    ATIVO = models.CharField(max_length=1)
    SETOR = models.CharField(max_length=100)  # Adicione este campo para armazenar o setor do usuário

    class Meta:
        managed = False
        db_table = 'OBERON.USUARIO'


class Sistema(models.Model):
    SISTEMA = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'OBERON.SISTEMA'


class Padaces(models.Model):
    PADACES = models.CharField(max_length=100)
    SISTEMA = models.ForeignKey(Sistema, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'OBERON.PADACES'


class Usuariopadaces(models.Model):
    USUARIO = models.ForeignKey(User, on_delete=models.CASCADE)
    PADACES = models.ForeignKey(Padaces, on_delete=models.CASCADE)

    # PERFIL = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'OBERON.USUARIOPADACES'


from django.db import migrations


def set_default_criador(apps, schema_editor):
    AtoNormativ = apps.get_model('core', 'AtoNormativ')
    User = apps.get_model('auth', 'User')
    default_criador = User.objects.get(pk=1)  # Defina o usuário com id=1 como criador padrão
    AtoNormativ.objects.update(criador=default_criador)


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),  # Substitua 'yourappname' pelo nome real do seu aplicativo
    ]

    operations = [
        migrations.RunPython(set_default_criador),
    ]
    
class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

class AssinantesBoletim(SingletonModel):
    reitor = models.CharField(max_length=100)
    vice_reitor = models.CharField(max_length=100)
    reitor_admin = models.CharField(max_length=100)
    reitor_pes_grad = models.CharField(max_length=100)
    reitor_ens = models.CharField(max_length=100)
    reitor_plan = models.CharField(max_length=100)
    reitor_int = models.CharField(max_length=100)
    reitor_ext = models.CharField(max_length=100)

    def __str__(self):
            return self.reitor
        
class AtoHash(models.Model):
    ato = models.ForeignKey(AtoNormativ, on_delete=models.CASCADE, related_name='ato_hashes')
    pdf_hash = models.CharField(max_length=64, unique=True)  # Use um campo apropriado para armazenar hashes
    pdf_file = models.FileField(upload_to='temp/', null=True, blank=True)
    
    def __str__(self):
        return self.pdf_hash