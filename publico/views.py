from django.shortcuts import render
from core.models import AtoNormativ, AtoHash
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse
from core.models import BoletimGerado
import cx_Oracle
from core.models import AtoNormativ
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.
import os
def geral(request):

    ato = AtoNormativ.objects.all()
    
    portaria = AtoNormativ.objects.filter(tipo_ato='portaria').filter(status="aprovado")
    resolucao = AtoNormativ.objects.filter(tipo_ato='Resolução').filter(status="aprovado")
    boletim = BoletimGerado.objects.filter(status='aprovado')

    for b in boletim:
        ato_normativ_index = b.conteudo_pdf.find('AtoNormativ:')
        if ato_normativ_index != -1:
            b.conteudo_pdf = b.conteudo_pdf.replace('AtoNormativ:', '')  
        b.conteudo_pdf = b.conteudo_pdf.strip('[<>]')

    anos_unicos = []

    for a in ato:
        ano = a.dt_cadastro.year
        
        if ano not in anos_unicos:
            anos_unicos.append(ano)

    anos_unicos.sort(reverse=True)

    return render(request, 'geral.html', {'portaria': portaria, 'boletim': boletim, 'resolucao': resolucao, 'anos':anos_unicos, })

def abrir_pdf(request):
    if request.method != "GET":

        return render(request, 'edit.html')

    elif request.method == "GET":
        hash = request.GET.get("hash")

    pdf = get_object_or_404(AtoHash, pdf_hash=hash)

    if pdf.pdf_file:
        pdf_path = os.path.join(pdf.pdf_file.name)  
        response = FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
        return response
    else:
        return render(request, 'pdf_not_found.html')  


def view_publico(request, ato_id):
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

    return render(request, 'view_publico.html', context)

def search_view(request):
    query = request.GET.get('texto', '')  
    results = AtoNormativ.objects.filter(        
        Q(tipo_ato__contains=query) |
        Q(texto_normativo__contains=query) 
    ).values().filter(status='aprovado')  

    boletim_results = BoletimGerado.objects.filter(
        Q(titulo__contains=query) |
        Q(conteudo_pdf__contains=query)
    ).all()


    return render(request, 'search_results.html', {'results': results, 'query': query, 'boletim_results': boletim_results})

# def advanced_filter(request):
    