from django.urls import path, include
from . import views
from .views import edit
from .views import salvar_ato
from .views import salvar_autoridade
from .views import view
from .views import editar_ato
# from .views import gerar_pdf
from .views import revisao
from .views import pendentes
from .views import GerarPDFView
from .views import view
from .views import aprovados
from . import views
from core import  views
from django.contrib.auth.decorators import login_required


# from .views import gerar_pdf
from .views import boletim



urlpatterns = [
    path('', views.index, name='index'),
    path('edit/', views.edit, name='edit'),
    #Ato View
    path('ato/<int:ato_id>/', views.view, name='view'),
    #View Boletim
    path('ato/<str:ato_ids>/', views.view_boletim, name='view_boletim'),
    #Salvar e Deletar Autoridade
    path('salvar_autoridade/', views.salvar_autoridade, name= 'salvar_autoridade'),
    path('delete_autoridade/<int:autoridade_id>/', views.delete_autoridade, name= 'delete_autoridade'),
    #Salvar Ato
    path('salvar/', views.salvar_ato, name = 'salvar_ato'),
    #Salvar Boletim
    path('salvar_boletim/<str:ato_ids>/', views.salvar_boletim, name='salvar_boletim'),
    #Gerar PDF/Portaria e Resolucao
    path('gerar_pdf/<int:ato_ids>/', GerarPDFView.as_view(), name='gerar_pdf'),
    path('gerar_pdf/<str:ato_ids>/<int:boletim_id>/', GerarPDFView.as_view(), name='gerar_pdf'),
    #Gerar PDF/Boletim
    path('gerar_boletim/<str:ato_ids>/<int:boletim_id>/', GerarPDFView.as_view(), name='gerar_boletim'),
    #Editar Ato
    path('ato/<int:ato_id>/editar/', views.editar_ato, name='editar_ato'),
    #Editar Boletim
    path('ato/<str:ato_ids>/editar/', views.editar_boletim, name='editar_boletim'),
    #Atos/Boletim
    path('aprovados/', views.aprovados, name='aprovados'),
    path('rascunhos/', views.rascunhos, name='rascunhos'),
    path('cancelados/', views.cancelados, name='cancelados'),
    path('revisao/', views.revisao, name='revisao'),
    path('pendentes/', views.pendentes, name='pendentes'),
    path('boletim/', views.boletim, name='boletim'),
    path('pesquisar/', views.pesquisar, name='pesquisar'),
    path('boletins_salvos/', views.boletins_salvos, name='boletins_salvos'),


]

 # path('gerar_pdf/<int:ato_id>/', views.gerar_pdf, name='gerar_pdf'),