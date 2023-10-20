from django.urls import path
from publico import views


urlpatterns = [
 
    path('geral/', views.geral, name='geral'),
    path('abrir_pdf/', views.abrir_pdf, name='abrir_pdf'),
    path('ato/<int:ato_id>/', views.view_publico, name='view_publico'),
    path('search/', views.search_view, name='search_results'),
]

