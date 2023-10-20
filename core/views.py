from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.html import strip_tags
from django.contrib import messages
from django.contrib.messages import constants
from io import BytesIO
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.contrib import messages
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.views.generic.edit import UpdateView
from core.models import AtoNormativ
from django.core.paginator import Paginator
from django.views import View
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import letter
from django.contrib.auth import logout
from reportlab.lib.pagesizes import letter
from datetime import datetime
from reportlab.lib import colors
from core.Portaria import Portaria
from core.Boletim import Boletim
from django.db.models import Q
from .models import BoletimGerado, AssinantesBoletim, AtoNormativ, Autoridade

from django.shortcuts import redirect
from django.utils.html import strip_tags
from django.contrib.messages import constants
from django.contrib import messages
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .models import Autoridade, OracleUser, Usuariopadaces
from django.core.paginator import Paginator
from django.views import View
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import letter
import cx_Oracle
from django.shortcuts import render, get_object_or_404
from .models import AtoNormativ, Padaces, Usuario, AtoHash
from django.utils.html import strip_tags
import hashlib
import tempfile
import os


def index(request):
    return render(request, 'index.html')
@login_required()
def view(request, ato_id):
    ato = get_object_or_404(AtoNormativ, pk=ato_id)

    # Verifica se o usuário tem PADACES 697
    padaces_aceitos = []
    setor_usuario = None

    if request.user.is_authenticated:

        # Configurações de conexão com o banco de dados Oracle
        db_settings = {
            'USER': 'cons_oberon',
            'PASSWORD': 'pwdconsoberon',
            'HOST': '10.70.0.14',
            'PORT': '1521',
            'SERVICE_NAME': 'prouea2',
        }

        # Estabelece a conexão com o banco de dados Oracle
        connection = cx_Oracle.connect(
            f"{db_settings['USER']}/{db_settings['PASSWORD']}@{db_settings['HOST']}:{db_settings['PORT']}/{db_settings['SERVICE_NAME']}"
        )

        cursor = connection.cursor()
        user_id = request.session['user_id'].split('=')[1]

        try:
            cursor.execute(f"SELECT * FROM OBERON.USUARIOPADACES WHERE USUARIO = '{user_id}' AND PADACES = 697")
            padaces_aceitos = cursor.fetchone()

            cursor.execute(f"SELECT SETOR FROM OBERON.USUARIO WHERE USER_LDAP = '{user_id}'")
            setor_row = cursor.fetchone()
            if setor_row:
                setor_usuario = setor_row[0]

            print('#####################')
            print(setor_usuario)
            print('#####################')

        finally:
            # Fecha o cursor e a conexão com o banco de dados
            cursor.close()
            connection.close()

    is_admin = padaces_aceitos is not None
    context = {'ato': ato, 'is_admin': is_admin, 'setor_usuario': setor_usuario}
    return render(request, 'view.html', context)


def view_boletim(request, ato_ids):
    boletim = get_object_or_404(BoletimGerado, portarias_fks=ato_ids)
    context = {'boletim': boletim}
    return render(request, 'view_boletim.html', context)


# def authetication(request):
#     return render(request, 'authentication.html')
def salvar_boletim(request, ato_ids):
    ato_ids_list = [int(id) for id in ato_ids.split(',')]

    # Criar o boletim combinando os atos selecionados
    atos_selecionados = []
    for ato_id in ato_ids_list:
        ato = get_object_or_404(AtoNormativ, id=ato_id)
        atos_selecionados.append(ato)
    ids_serializados = ','.join(str(id) for id in ato_ids_list)
    print(ids_serializados)
    # Salvar o PDF gerado no banco de dados
    boletim = BoletimGerado.objects.create(
        portarias_fks=ids_serializados,
        titulo=f"Boletim - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        conteudo_pdf=atos_selecionados,
        status='revisao'
    )
    {"boletim_id": boletim.id}
    print(boletim.id)
    messages.add_message(request, constants.SUCCESS, 'Boletim salvo com sucesso.')
    return redirect('revisao')


# @login_required
def edit(request):
    # Verificar se o usuário tem permissões PADACES 697
    is_admin = False  # Defina inicialmente como não administrador

    if request.user.is_authenticated:

        # Configurações de conexão com o banco de dados Oracle
        db_settings = {
            'USER': 'cons_oberon',
            'PASSWORD': 'pwdconsoberon',
            'HOST': '10.70.0.14',
            'PORT': '1521',
            'SERVICE_NAME': 'prouea2',
        }

        # Estabelece a conexão com o banco de dados Oracle
        connection = cx_Oracle.connect(
            f"{db_settings['USER']}/{db_settings['PASSWORD']}@{db_settings['HOST']}:{db_settings['PORT']}/{db_settings['SERVICE_NAME']}"
        )

        cursor = connection.cursor()
        user_id = request.session['user_id'].split('=')[1]

        try:
            cursor.execute(f"SELECT * FROM OBERON.USUARIOPADACES WHERE USUARIO = '{user_id}' AND PADACES = 697")
            padaces_aceitos = cursor.fetchone()

        finally:
            # Fecha o cursor e a conexão com o banco de dados
            cursor.close()
            connection.close()

        is_admin = padaces_aceitos is not None  # Verifica se é administrador

    # Continue com o código para obter os atos normativos e autoridades e renderizar a página
    atonormativs = AtoNormativ.objects.all()
    autoridades = Autoridade.objects.all()

    return render(request, 'edit.html', {
        'atonormativs': atonormativs,
        'autoridades': autoridades,
        'is_admin': is_admin,  # Passe a variável is_admin para o template
    })



def calcular_hash_do_ato(ato):
    dados_para_hash = (
        f"{ato.texto_normativo}{ato.ementa}{ato.ano}{ato.numero}{ato.doe_pagina}{ato.doe_secao}"
        f"{ato.doe_numero}{ato.autoridade1}{ato.autoridade2}{ato.tipo_ato}{ato.assinante1_id}{ato.assinante2_id}"
    )
    hash_obj = hashlib.sha256(dados_para_hash.encode())
    pdf_hash = hash_obj.hexdigest()
    return pdf_hash

# @login_required
def salvar_ato(request):
    if request.method != "POST":
        return render(request, 'edit.html')

    elif request.method == "POST":
        textoNormativo = request.POST.get("textoNormativo")
        textoEmenta = request.POST.get("textoEmenta")
        nomeAutoridadeAssinantePrimaria = request.POST.get("nomeAutoridadeAssinantePrimaria")
        nomeAutoridadeAssinanteSecundaria = request.POST.get("nomeAutoridadeAssinanteSecundaria")
        tipoAto = request.POST.get("tipoAto")
        numeroAto = request.POST.get("numeroAto")
        cargoDaAutoridadePrimaria = request.POST.get("cargoDaAutoridadePrimaria")
        cargoDaAutoridadeSecundaria = request.POST.get("cargoDaAutoridadeSecundaria")
        textoNormativoSantinizado = strip_tags(textoNormativo)
        textoEmentaSanitizado = strip_tags(textoEmenta)

        try:
            nomeAutoridadeAssinantePrimaria = Autoridade.objects.get(id=nomeAutoridadeAssinantePrimaria)

            # Obter o setor do usuário logado
            setor_usuario = None
            if request.user.is_authenticated:
                db_settings = {
                    'USER': 'cons_oberon',
                    'PASSWORD': 'pwdconsoberon',
                    'HOST': '10.70.0.14',
                    'PORT': '1521',
                    'SERVICE_NAME': 'prouea2',
                }

                connection = cx_Oracle.connect(
                    f"{db_settings['USER']}/{db_settings['PASSWORD']}@{db_settings['HOST']}:{db_settings['PORT']}/{db_settings['SERVICE_NAME']}"
                )

                cursor = connection.cursor()
                user_id = request.session['user_id'].split('=')[1]

                try:
                    cursor.execute(f"SELECT SETOR FROM OBERON.USUARIO WHERE USER_LDAP = '{user_id}'")
                    setor_row = cursor.fetchone()
                    if setor_row:
                        setor_usuario = setor_row[0]

                finally:
                    cursor.close()
                    connection.close()

            # Lidar com campos nulos adequadamente para assinante2
            if nomeAutoridadeAssinanteSecundaria:
                nomeAutoridadeAssinanteSecundaria = Autoridade.objects.get(id=nomeAutoridadeAssinanteSecundaria)
            # Lidar com campos nulos adequadamente para autoridade2
            if nomeAutoridadeAssinanteSecundaria is not None:
                cargoDaAutoridadeSecundaria = cargoDaAutoridadeSecundaria

            # Lidar com campos nulos adequadamente para numeroAto
            if numeroAto:
                numeroAto = int(numeroAto)
            else:
                numeroAto = None

            # Salvar os dados no banco de dados
            AtoNormativ.objects.create(
                texto_normativo=textoNormativoSantinizado,
                ementa=textoEmentaSanitizado,
                numero=numeroAto,
                assinante1=nomeAutoridadeAssinantePrimaria,
                assinante2=nomeAutoridadeAssinanteSecundaria,
                autoridade1=cargoDaAutoridadePrimaria,
                autoridade2=cargoDaAutoridadeSecundaria,
                tipo_ato=tipoAto,
                status='revisao',
                criador=request.user.username.split('@')[0],
                dt_cadastro=timezone.now(),
                setores_uea=setor_usuario  # Salvar o setor do usuário no campo setores_uea
            )
            
            messages.success(request, 'Ato salvo com sucesso.')
            return redirect('revisao')

        except:
            messages.warning(request, 'O sistema apresenta falhas internas.')
            return redirect('../edit/')


@login_required
def salvar_autoridade(request):

    if request.method != "POST":
        return render(request, 'edit.html')

    elif request.method == "POST":
        autoridade = request.POST.get("nomeAutoridade")

        Autoridade.objects.create(
            nome=autoridade,
        )
        return redirect('edit')


def mm2p(milimetros):
    return milimetros / 0.352777


def mm2p(mm_value):
    return mm_value * 2.83465


class GerarPDFView(View):

    def get(self, request, ato_ids, boletim_id):

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="documento.pdf"'
        packet = BytesIO()


        if isinstance(ato_ids, str) and ',' in ato_ids:
            
            boletim = Boletim()         
            pdf = canvas.Canvas(packet)
            ato_ids_list = [int(id) for id in ato_ids.split(',')]
            atos = []
            for i in ato_ids_list:
                atos.append(get_object_or_404(AtoNormativ, id=i))
            boletins = get_object_or_404(BoletimGerado, id=boletim_id)
            ass = get_object_or_404(AssinantesBoletim, id=1)
            



            boletim_path = 'templates/static/images/boletim.jpg'
            # antes: '/home/gabriel/Documentos/uea-news/templates/static/images/boletim.jpg'
            # '/home/lury/Área de Trabalho/projeto/uea-news/templates/static/images/logo-governo.jpg'
            CAPA_TITULO = "BOLETIM N°" + str(boletins.id)

            boletim.desenharCapa(pdf, boletim_path, CAPA_TITULO)

            def add_page():
                pdf.showPage()
                boletim.draw_header(pdf)

            conta_cata_subtitulo = 'UNIVERSIDADE DO ESTADO DO AMAZONAS'
            doe = CAPA_TITULO
            boletim.desenharContraCapa(pdf, doe, conta_cata_subtitulo)

            assinante_unicas = []
            autoridade = ""
            asdf = 620
            y = 600
            def format_value(value):
                return str(value).strip("(),''")

            pdf.setFont('Helvetica', 12)

            fields = [
                ('Reitor', ass.reitor),
                ('Vice-Reitora', ass.vice_reitor),
                ('Pró-Reitor de Administração', ass.reitor_admin),
                ('Pró-Reitor de Pesquisa e Pós-Graduação', ass.reitor_pes_grad),
                ('Pró-Reitor de Ensino de Graduação', ass.reitor_ens),
                ('Pró-Reitora de Planejamento', ass.reitor_plan),
                ('Pró-Reitor de Interiorização', ass.reitor_int),
                ('Pró-Reitor de Extensão e Assuntos Comunitários', ass.reitor_ext)
            ]
            x = 260
            for field_name, value in fields:
                formatted_value = format_value(value)
                pdf.drawString(210, asdf - 10, formatted_value)
                asdf -= 30
                pdf.setFont('Helvetica-Bold', 12)
                pdf.drawString(x, asdf, field_name)
                x -= 10
                pdf.setFont('Helvetica', 12)
            pdf.setFont('Helvetica-Bold', 12)
            asdf -= 20

            pdf.drawString(280, asdf, 'Comunitários')
            
         

            add_page()

            y = 650 
           
            boletim.desenharSumario(pdf, doe, conta_cata_subtitulo)
            for ato in atos:

                ato_posicao = pdf.stringWidth(ato.tipo_ato, 'Helvetica-Bold', 12)

                data_str = str(ato.doe_data)
                ano = data_str[0:4]

                doe_str = str(ato.numero)
                doe = "PORTARIA N°" + doe_str + "/" + ano
                pdf.setFont('Helvetica-Bold', 12)
                pdf.drawString(180, y, doe)
                pdf.setFont("Helvetica", 12)
                y -= 20 
            add_page()

            
            
            x = 70
            y = 650
            tamanho_fonte = 12
            limite_largura = 520
            limite_altura = 100
            espacamento_margem = 10  # Espaçamento desejado para as margens

        
            for ato in atos:
                assinatura = str(ato.assinante1).split('/')[0]
                assinatura2 = ato.assinante2

                paragrafos = ato.texto_normativo.splitlines()
                for index, paragrafo in enumerate(paragrafos):
                    if index == 0:
                        pdf.setFont("Helvetica-Bold", 12)
                        pdf.drawString(240, y, ato.tipo_ato.upper())

                        ato_posicao = pdf.stringWidth(ato.tipo_ato, 'Helvetica-Bold', 12)
                        n_posicao = 304 + ato_posicao + -43
                        limite_x = 550  # Limite horizontal do documento
                        if n_posicao > limite_x:
                            n_posicao = limite_x

                        data_str = str(ato.doe_data)
                        ano = data_str[0:4]

                        doe_str = str(ato.numero)
                        doe = "N°" + doe_str + "/" + ano

                        pdf.setFont('Helvetica-Bold', 12)
                        pdf.drawString(n_posicao, y, doe)
                        pdf.setFont("Helvetica", 12)

                        y -= tamanho_fonte + 2

                    if y - tamanho_fonte < limite_altura:
                        add_page()
                        y = 650

                    # Calcular a largura disponível considerando a margem esquerda e a margem direita
                    largura_disponivel = limite_largura - x

                    if pdf.stringWidth(paragrafo, 'Helvetica', 12) > largura_disponivel:
                        # Verificar se o parágrafo completo cabe na página atual
                        palavras = paragrafo.split(' ')
                        paragrafo_temp = ''
                        for palavra in palavras:
                            if pdf.stringWidth(paragrafo_temp + palavra, 'Helvetica', 12) < largura_disponivel:
                                paragrafo_temp += palavra + ' '
                            else:
                                # Desenhar o parágrafo atual
                                pdf.drawString(x, y, paragrafo_temp)
                                # Atualizar a posição vertical para o próximo parágrafo
                                y -= tamanho_fonte + 2
                                paragrafo_temp = palavra + ' '

                        # Desenhar o restante do parágrafo
                        pdf.drawString(x, y, paragrafo_temp)
                    else:
                        # Desenhar o parágrafo completo
                        pdf.drawString(x, y, paragrafo)

                    if index == len(paragrafos) - 1:
                                # Desenhar a assinatura apenas uma vez no final do parágrafo
                        y_assinatura = y - tamanho_fonte - 1
                        pdf.setFont("Helvetica-Bold", 12)
                        pdf.drawString(200, y_assinatura, assinatura.upper())
                        y = y_assinatura - 15 
                        pdf.setFont('Helvetica', 12)
                        pdf.drawString(180,y, 'UNIVERSIDADE DO ESTADO DO AMAZONAS')
                    y -= tamanho_fonte + 2                    
                    pdf.setFont("Helvetica-Bold", 12)
                    pdf.drawString(250, 750, CAPA_TITULO)
                    data_str = str(ato.doe_data)
                    ano = data_str[0:4]

                    pdf.setFont('Helvetica', 12)
                    pdf.drawString(180, 730, 'UNIVERSIDADE DO ESTADO DO AMAZONAS')
                    pdf.drawString(300,25, f"{pdf.getPageNumber() + 1}")
                y -= espacamento_margem 
                final_pdf_path = f"core/temp/boletim_{ato.id}.pdf"

        else:
          
            portaria = Portaria()
            ato = get_object_or_404(AtoNormativ, id=int(ato_ids))
            pdf = canvas.Canvas(packet, pagesize=letter)       

            ato_hash = AtoHash.objects.filter(ato=ato).first()
            if ato_hash:
                hash = ato_hash.pdf_hash  
                pdf.setFont('Helvetica', 7)

                pdf.drawString(50, 50, "Chave Autenticadora Hash: " + hash) 

        
            FONT = "Helvetica"
            FONT_BOLD = "Helvetica-Bold"
            font_size2 = 8

            pdf.setFont(FONT_BOLD, 12)

            data_str = str(ato.doe_data)
            ano = data_str[0:4]
            numero = str(ato.numero)

            if numero == "None":
                numero = "TESTE"

            doe = " N°" + numero + "/" + ano

            pdf.drawString(240, 680, ato.tipo_ato.upper() + doe)

            def add_page():
                pdf.showPage()
                portaria.draw_header(pdf)
                portaria.draw_footer(pdf)
            
            limite_largura = 550
            limite_altura = 100

            MARGIN_LEFT = 50
            MARGIN_BOTTOM = 650  
            tamanho_fonte = 10

            portaria.draw_header(pdf)
            portaria.draw_footer(pdf)

            palavras = ato.texto_normativo.split()

            for palavra in palavras:
                largura_palavra = pdf.stringWidth(palavra, FONT, tamanho_fonte)

                if MARGIN_LEFT + largura_palavra < limite_largura:
                    pdf.drawString(MARGIN_LEFT, MARGIN_BOTTOM, palavra )
                    MARGIN_LEFT += largura_palavra + pdf.stringWidth(" ", FONT, tamanho_fonte)
                else:
                    MARGIN_LEFT = 50
                    MARGIN_BOTTOM -= tamanho_fonte 

                    if MARGIN_BOTTOM < limite_altura:
                        add_page()
                        MARGIN_BOTTOM = 700

                    pdf.drawString(MARGIN_LEFT, MARGIN_BOTTOM, palavra + " ")
                    MARGIN_LEFT += largura_palavra + pdf.stringWidth("", FONT, tamanho_fonte)


            assinante = str(ato.assinante1).split('/')[0]

            altura_texto_embaixo = pdf.stringWidth(assinante, FONT, 12)

            y_embaixo = MARGIN_BOTTOM - tamanho_fonte + 5 - altura_texto_embaixo - -20  
            y_abaixo = MARGIN_BOTTOM - tamanho_fonte + 5 - altura_texto_embaixo - -9
        

            pdf.setFont(FONT_BOLD, 12)

            largura_assinante = pdf.stringWidth(assinante, FONT_BOLD, 12)

            y_assinante = y_embaixo + tamanho_fonte 

            y_autoridade = y_abaixo + tamanho_fonte 

            def centralizar(text):
                return ((letter[0] - text) / 2)

            pdf.drawString(centralizar(largura_assinante), y_assinante, assinante.upper())

            TEXTO_FUNCAO = ato.autoridade1 + " Da Universidade Do Estado Do Amazonas"
            
            largura_autoridade = pdf.stringWidth(TEXTO_FUNCAO, FONT, 12)

            pdf.setFont(FONT, 12)

            pdf.drawString(centralizar(largura_autoridade), y_autoridade, TEXTO_FUNCAO)
            
            DATE_MARGIN_X = 50
            altura_texto_embaixo = pdf.stringWidth(assinante, FONT, 12)

            y_outro = MARGIN_BOTTOM - tamanho_fonte  - altura_texto_embaixo - -10

            data_objeto = datetime.strptime(data_str[:10], "%Y-%m-%d")
            data_br = data_objeto.strftime("%d-%m-%Y")
            

            TEXT_ASSINATURA = "Assinado por: " + assinante 
            TEXT_DATE = f"Data: {data_br}"

            DATA_POSITION_Y = y_outro - 10

            pdf.setFont(FONT, font_size2)

            pdf.drawString(DATE_MARGIN_X, y_outro, TEXT_ASSINATURA)
            pdf.drawString(DATE_MARGIN_X, DATA_POSITION_Y, TEXT_DATE)

            assinante2 = str(ato.assinante2).split('/')[0]

            if ato.assinante2 != None:

                TEXT_ASSINATURA = "Assinado por: " + assinante2
                TEXT_DATE = f"Data: {data_br}"
                
                y_o = MARGIN_BOTTOM - tamanho_fonte - altura_texto_embaixo - 20

                DATA_POSITION_Y = y_o - 10

                pdf.setFont(FONT, font_size2)

                pdf.drawString(DATE_MARGIN_X, y_o, TEXT_ASSINATURA)
                pdf.drawString(DATE_MARGIN_X, DATA_POSITION_Y, TEXT_DATE)
                final_pdf_path = f"core/temp/ato_{ato.id}.pdf"


  
        pdf.save()
        


        with open(final_pdf_path, 'wb') as pdf_file:
            pdf_file.write(packet.getvalue())

        response.write(packet.getvalue())
        return response
    
def format_value(value):
    return str(value).strip("(),''")
        
@login_required
def editar_boletim(request, ato_ids):

    ato = get_object_or_404(BoletimGerado, portarias_fks=ato_ids)
    ass = get_object_or_404(AssinantesBoletim, id=1)
    
    reitor = format_value(ass.reitor)
    vice_reitor = format_value(ass.vice_reitor)
    reitor_admin = format_value(ass.reitor_admin)
    reitor_pes_grad = format_value(ass.reitor_pes_grad)
    reitor_ens = format_value(ass.reitor_ens)
    reitor_plan = format_value(ass.reitor_plan)
    reitor_int = format_value(ass.reitor_int)
    reitor_ext = format_value(ass.reitor_ext)
    
    if request.method == 'POST':
        assinante = AssinantesBoletim.objects.first()
        assinante.reitor = request.POST.get('reitor'),
        assinante.vice_reitor = request.POST.get('vice_reitor'),
        assinante.reitor_admin = request.POST.get('reitor_admin'),
        assinante.reitor_pes_grad = request.POST.get('reitor_pes_grad'),
        assinante.reitor_ens = request.POST.get('reitor_ens'),
        assinante.reitor_plan = request.POST.get('reitor_plan'),
        assinante.reitor_int = request.POST.get('reitor_plan'),
        assinante.reitor_ext= request.POST.get('reitor_ext'),
        assinante.save()
        ato.status = request.POST.get('status')
       
        ato.save()
        return redirect('boletins_salvos')

    context = {
        'ato': ato, 'reitor': reitor, 
        'vice_reitor': vice_reitor,
        'reitor_admin': reitor_admin,
        'reitor_pes_grad':reitor_pes_grad,
        'reitor_ens': reitor_ens,
        'reitor_plan':reitor_plan,
        'reitor_int': reitor_int,
        'reitor_ext': reitor_ext}
    return render(request, 'editar_boletim.html', context)


def delete_autoridade(request, autoridade_id):

    autoridade = get_object_or_404(Autoridade, id=autoridade_id)

    autoridade.delete()

    return redirect('edit')


@login_required
def editar_ato(request, ato_id):
    ato = get_object_or_404(AtoNormativ, pk=ato_id)

    if request.method == 'POST':
        ato.texto_normativo = request.POST.get('texto_normativo')
        ato.ementa = request.POST.get('ementa')
        ato.ano = request.POST.get('ano')

        # Verifique se o número é fornecido no formulário
        numero = request.POST.get('numero')
        ato.numero = int(numero) if numero is not None and numero != 'None' and numero != '' else None

        ato.doe_pagina = request.POST.get('doe_pagina')
        ato.doe_secao = request.POST.get('doe_secao')
        ato.doe_numero = request.POST.get('doe_numero')

        autoridade1 = request.POST.get('autoridade1')
        autoridade2 = request.POST.get('autoridade2')

        ato.autoridade1 = autoridade1 if autoridade1 else 'setor'
        ato.autoridade2 = autoridade2 if autoridade2 else 'setor'

        assinante1_id = request.POST.get('assinante1')
        ato.assinante1_id = assinante1_id if assinante1_id else None

        ato.tipo_ato = request.POST.get('tipo_ato')

        assinante2_id = request.POST.get('assinante2')
        ato.assinante2_id = assinante2_id if assinante2_id else None

        ato.status = request.POST.get('status')
        ato.pendestes_texto = request.POST.get('pendente')

        if ato.status == 'PENDENTE':
            ato.pendencia = request.POST.get('pendencia')
            if request.POST.get('atualizar'):
                ato.status = 'revisao'
        else:
            ato.pendencia = None

        if ato.status == 'aprovado':
            pdf_hash = calcular_hash_do_ato(ato)
            print(pdf_hash)
            pdf_file_path = f"core/temp/ato_{ato.id}.pdf"

            if os.path.exists(pdf_file_path):
                # Crie um arquivo temporário para armazenar o conteúdo do PDF
                with tempfile.NamedTemporaryFile(delete=False) as temp_pdf_file:
                    with open(pdf_file_path, 'rb') as pdf_file:
                        temp_pdf_file.write(pdf_file.read())

                # Salve o conteúdo do PDF como um arquivo temporário
                AtoHash.objects.create(ato=ato, pdf_hash=pdf_hash, pdf_file=temp_pdf_file.name)

                print(f"PDF Hash: {pdf_hash}")
            else:
                print(f"Arquivo PDF não encontrado para o ato com ID {ato.id}")

        ato.save()
        messages.success(request, 'Ato atualizado com sucesso.')
        return redirect('view', ato_id=ato.id)

    assinantes = Autoridade.objects.all()
    if request.POST.get('aprovar_ato'):
        ato.status = 'aprovado'
        ato.save()
        return redirect('main')

    context = {'ato': ato, 'assinantes': assinantes}
    return render(request, 'editar_ato.html', context)


def paginar(list, limit_per_page, request):
    paginator = Paginator(list, limit_per_page)
    page = request.GET.get('page')
    atos = paginator.get_page(page)
    context = {'atos': atos}
    return context


# @login_required
def aprovados(request):
    setor_usuario = None

    # Obtém o setor do usuário logado (mesma lógica que em revisao)
    if request.user.is_authenticated:
        db_settings = {
            'USER': 'cons_oberon',
            'PASSWORD': 'pwdconsoberon',
            'HOST': '10.70.0.14',
            'PORT': '1521',
            'SERVICE_NAME': 'prouea2',
        }

        connection = cx_Oracle.connect(
            f"{db_settings['USER']}/{db_settings['PASSWORD']}@{db_settings['HOST']}:{db_settings['PORT']}/{db_settings['SERVICE_NAME']}"
        )

        cursor = connection.cursor()
        user_id = request.session['user_id'].split('=')[1]

        try:
            cursor.execute(f"SELECT SETOR FROM OBERON.USUARIO WHERE USER_LDAP = '{user_id}'")
            setor_row = cursor.fetchone()
            if setor_row:
                setor_usuario = setor_row[0]

        finally:
            cursor.close()
            connection.close()

    # Filtra os atos aprovados por setor (caso o setor do usuário esteja definido)
    results = AtoNormativ.objects.all()
    if setor_usuario:
        results = results.filter(setores_uea=setor_usuario)

   
    # Cria o paginator para os atos aprovados
    paginator_atos = Paginator(results, 10)
    page_number_atos = request.GET.get('page_atos')
    atos_page = paginator_atos.get_page(page_number_atos)


    anos_unicos = []

    for a in results:
        ano = a.dt_cadastro.year
        
        if ano not in anos_unicos:
            anos_unicos.append(ano)

    anos_unicos.sort(reverse=True)

    ato = request.GET.get('ato')
    ementa = request.GET.get('ementa')
    autoridade = request.GET.get('autoridade')
    assinante = request.GET.get('assinante')
    status = request.GET.get('status')

    results = results.filter(
        Q(tipo_ato__icontains=ato)|
        Q(texto_normativo__icontains=ementa)|
        Q(autoridade1__icontains=autoridade)|
        Q(assinante1__icontains=assinante)|
        Q(status=status)
        )
    # if ementa:
    #     results = results.filter()
    # if autoridade:
    #     results = results.filter(autoridade1__icontains=autoridade)
    # if assinante:
    #     results = results.filter(assinante1__icontains=assinante)
    # if status:
    #     results = results.filter(status=status)
    
    values = []

    context = {
        'atos': results,
        'anos':anos_unicos,
    }

    return render(request, 'main.html', context)

def filter_url(request):
    results = AtoNormativ.objects.all()
    ato = request.GET.get('ato', '')
    ementa = request.GET.get('ementa', '')
    autoridade = request.GET.get('autoridade', '')
    assinante = request.GET.get('assinante', '')
    status = request.GET.get('status', '')
    
    if ato:
        results = results.filter(ato__icontains=ato)
    if ementa:
        results = results.filter(ementa__icontains=ementa)
    if autoridade:
        results = results.filter(autoridade1__icontains=autoridade)
    if assinante:
        results = results.filter(assinante1__icontains=assinante)
    if status:
        results = results.filter(status=status)


    context = {
        'atos': results,
    }
    
    return render(request, 'main.html', context)

def boletim(request):
    atos_list = AtoNormativ.objects.filter(status='aprovado')


    anos_unicos = []

    for a in atos_list:
        ano = a.dt_cadastro.year
        
        if ano not in anos_unicos:
            anos_unicos.append(ano)

    anos_unicos.sort(reverse=True)


    # Combinando os dois contextos em um único dicionário
    context = {'atos':atos_list, 'anos':anos_unicos}

    return render(request, 'boletim.html', context)


# @login_required
def cancelados(request):
    setor_usuario = None

    # Obtém o setor do usuário logado (mesma lógica que em revisao)
    if request.user.is_authenticated:
        db_settings = {
            'USER': 'cons_oberon',
            'PASSWORD': 'pwdconsoberon',
            'HOST': '10.70.0.14',
            'PORT': '1521',
            'SERVICE_NAME': 'prouea2',
        }

        connection = cx_Oracle.connect(
            f"{db_settings['USER']}/{db_settings['PASSWORD']}@{db_settings['HOST']}:{db_settings['PORT']}/{db_settings['SERVICE_NAME']}"
        )

        cursor = connection.cursor()
        user_id = request.session['user_id'].split('=')[1]

        try:
            cursor.execute(f"SELECT * FROM OBERON.USUARIOPADACES WHERE USUARIO = '{user_id}' AND PADACES = 697")
            padaces_aceitos = cursor.fetchone()

            cursor.execute(f"SELECT SETOR FROM OBERON.USUARIO WHERE USER_LDAP = '{user_id}'")
            setor_row = cursor.fetchone()
            if setor_row:
                setor_usuario = setor_row[0]

        finally:
            cursor.close()
            connection.close()

    is_admin = padaces_aceitos is not None

    # Filtra os atos cancelados por setor (caso o setor do usuário esteja definido)
    atos_cancelados = AtoNormativ.objects.filter(status='cancelado')
    if not is_admin and setor_usuario:
        atos_cancelados = atos_cancelados.filter(setores_uea=setor_usuario)

    # Cria o paginator para os atos cancelados
    paginator_atos = Paginator(atos_cancelados, 16)
    page_number_atos = request.GET.get('page_atos')
    atos_page = paginator_atos.get_page(page_number_atos)

    context = {
        'atos': atos_page,
    }

    return render(request, 'main.html', context)



# @login_required
def rascunhos(request):
    atos_list = AtoNormativ.objects.filter(status='rascunho')
    context = paginar(atos_list, 16, request);
    return render(request, 'main.html', context)


def revisao(request):
    setor_usuario = None
    is_admin = False  # Definir inicialmente como não administrador

    if request.user.is_authenticated:
        db_settings = {
            'USER': 'cons_oberon',
            'PASSWORD': 'pwdconsoberon',
            'HOST': '10.70.0.14',
            'PORT': '1521',
            'SERVICE_NAME': 'prouea2',
        }

        connection = cx_Oracle.connect(
            f"{db_settings['USER']}/{db_settings['PASSWORD']}@{db_settings['HOST']}:{db_settings['PORT']}/{db_settings['SERVICE_NAME']}"
        )

        cursor = connection.cursor()
        user_id = request.session['user_id'].split('=')[1]

        try:
            cursor.execute(f"SELECT * FROM OBERON.USUARIOPADACES WHERE USUARIO = '{user_id}' AND PADACES = 697")
            padaces_aceitos = cursor.fetchone()

            cursor.execute(f"SELECT SETOR FROM OBERON.USUARIO WHERE USER_LDAP = '{user_id}'")
            setor_row = cursor.fetchone()
            if setor_row:
                setor_usuario = setor_row[0]

        finally:
            cursor.close()
            connection.close()

        is_admin = padaces_aceitos is not None  # Verifica se é administrador

    if is_admin:
        atos_list = AtoNormativ.objects.filter(status='revisao')
        boletim_list = BoletimGerado.objects.filter(status='revisao')
    else:
        atos_list = AtoNormativ.objects.filter(setores_uea=setor_usuario, status='revisao')
        boletim_list = BoletimGerado.objects.filter(status='revisao')

    # Create paginator for atos
    paginator_atos = Paginator(atos_list, 5)
    page_number_atos = request.GET.get('page_atos')
    atos_page = paginator_atos.get_page(page_number_atos)

    # Create paginator for boletins
    paginator_boletins = Paginator(boletim_list, 5)
    page_number_boletins = request.GET.get('page_boletins')
    boletins_page = paginator_boletins.get_page(page_number_boletins)

    anos_unicos = []

    for a in atos_list:
        ano = a.dt_cadastro.year
        
        if ano not in anos_unicos:
            anos_unicos.append(ano)

    anos_unicos.sort(reverse=True)
    context = {
        'atos': atos_page,
        'boletim': boletins_page,
        'anos':anos_unicos,
    }

    return render(request, 'main.html', context)



# @login_required
def pendentes(request):
    setor_usuario = None

    # Obtém o setor do usuário logado (mesma lógica que em revisao)
    if request.user.is_authenticated:
        db_settings = {
            'USER': 'cons_oberon',
            'PASSWORD': 'pwdconsoberon',
            'HOST': '10.70.0.14',
            'PORT': '1521',
            'SERVICE_NAME': 'prouea2',
        }

        connection = cx_Oracle.connect(
            f"{db_settings['USER']}/{db_settings['PASSWORD']}@{db_settings['HOST']}:{db_settings['PORT']}/{db_settings['SERVICE_NAME']}"
        )

        cursor = connection.cursor()
        user_id = request.session['user_id'].split('=')[1]

        try:
            cursor.execute(f"SELECT * FROM OBERON.USUARIOPADACES WHERE USUARIO = '{user_id}' AND PADACES = 697")
            padaces_aceitos = cursor.fetchone()

            cursor.execute(f"SELECT SETOR FROM OBERON.USUARIO WHERE USER_LDAP = '{user_id}'")
            setor_row = cursor.fetchone()
            if setor_row:
                setor_usuario = setor_row[0]

        finally:
            cursor.close()
            connection.close()

    is_admin = padaces_aceitos is not None

    # Filtra os atos pendentes por setor (caso o setor do usuário esteja definido)
    atos_pendentes = AtoNormativ.objects.filter(status='PENDENTE')
    if not is_admin and setor_usuario:
        atos_pendentes = atos_pendentes.filter(setores_uea=setor_usuario)

    # Cria o paginator para os atos pendentes
    paginator_atos = Paginator(atos_pendentes, 16)
    page_number_atos = request.GET.get('page_atos')
    atos_page = paginator_atos.get_page(page_number_atos)

    context = {
        'atos': atos_page,
    }

    return render(request, 'main.html', context)



def pesquisar(request):
    if request.method == 'GET':
        termo_pesquisa = request.GET.get('pesquisa', '')  # Obtém o termo de pesquisa do parâmetro GET 'pesquisa'
        atos = AtoNormativ.objects.filter(
            texto_normativo__icontains=termo_pesquisa)  # Filtra os atos com base no termo de pesquisa
        context = {'atos': atos}
        return render(request, 'resultado_pesquisa.html', context)


def boletins_salvos(request):
    boletim = BoletimGerado.objects.all()
    for b in boletim:
        ato_normativ_index = b.conteudo_pdf.find('AtoNormativ:')
        if ato_normativ_index != -1:
            b.conteudo_pdf = b.conteudo_pdf[ato_normativ_index + len('AtoNormativ:'):]
        else:
            b.conteudo_pdf = b.conteudo_pdf

        anos_unicos = []

    for a in boletim:
        ano = a.data_criacao.year
        
        if ano not in anos_unicos:
            anos_unicos.append(ano)

    anos_unicos.sort(reverse=True)

    return render(request, 'boletins_salvos.html', {'boletim': boletim, 'anos':anos_unicos})


def get_oracle_users(request):
    # Configurações de conexão com o banco de dados Oracle
    db_settings = {
        'USER': 'cons_oberon',
        'PASSWORD': 'pwdconsoberon',
        'HOST': '10.70.0.14',
        'PORT': '1521',
        'SERVICE_NAME': 'prouea2',
    }

    # Estabelece a conexão com o banco de dados Oracle
    connection = cx_Oracle.connect(
        f"{db_settings['USER']}/{db_settings['PASSWORD']}@{db_settings['HOST']}:{db_settings['PORT']}/{db_settings['SERVICE_NAME']}"
    )

    # Cria um cursor para executar consultas
    cursor = connection.cursor()

    try:
        # Executa uma consulta para obter os nomes do campo USER_LDAP da tabela USUARIO no esquema OBERON
        cursor.execute("SELECT USUARIO FROM OBERON.USUARIOPADACES")

        # Recupera todos os registros retornados pela consulta
        results = cursor.fetchall()

        # Lista para armazenar os nomes de usuário
        usernames = [row[0] for row in results]

        # Renderiza o template 'edit.html' com os nomes de usuário
        return render(request, 'edit.html', {'usernames': usernames})

    finally:
        # Fecha o cursor e a conexão com o banco de dados
        cursor.close()
        connection.close()


def get_oracle_users(request):
    # Configurações de conexão com o banco de dados Oracle
    db_settings = {
        'USER': 'cons_oberon',
        'PASSWORD': 'pwdconsoberon',
        'HOST': '10.70.0.14',
        'PORT': '1521',
        'SERVICE_NAME': 'prouea2',
    }

    # Estabelece a conexão com o banco de dados Oracle
    connection = cx_Oracle.connect(
        f"{db_settings['USER']}/{db_settings['PASSWORD']}@{db_settings['HOST']}:{db_settings['PORT']}/{db_settings['SERVICE_NAME']}"
    )

    # Cria um cursor para executar consultas
    cursor = connection.cursor()

    try:
        # Executa uma consulta para obter os nomes do campo USER_LDAP da tabela USUARIO no esquema OBERON
        cursor.execute("SELECT USUARIO FROM OBERON.USUARIOPADACES")

        # Recupera todos os registros retornados pela consulta
        results = cursor.fetchall()

        # Lista para armazenar os nomes de usuário
        usernames = [row[0] for row in results]

        # Renderiza o template 'edit.html' com os nomes de usuário
        return render(request, 'edit.html', {'usernames': usernames})

    finally:
        # Fecha o cursor e a conexão com o banco de dados
        cursor.close()
        connection.close()



