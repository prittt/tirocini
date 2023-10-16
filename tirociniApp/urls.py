from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'tirociniApp'
urlpatterns = [
    path('', views.next_page, name='next'),
    path('homepage/', views.homepage, name='homepage'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('modulo/', views.RichiestaCreateView.as_view(), name='richiesta'),
    path('richiestaComp/', views.RichiestaDetailView.as_view(), name='richiestaComp'),
    path('success/', views.success, name='success'),
    path('archivio/', views.RichiestaListView.as_view(), name='archivio_richieste'),
    path('gestione/<int:pk>/', views.GestioneRichiestaView.as_view(), name='gestione'),
    path('update/<int:richiesta_id>/', views.update_state, name='update'),
    path('redirect/', views.next_page, name='redirect'),
    path('generate/', views.generate_pdf, name='generate'),
    path('discard/<int:richiesta_id>/', views.discard, name='delete'),
    path('access/', views.access, name="access"),
    path('AdministrationLogin/', views.adminLogin,name="loginAdmin"),
    path('review/<int:pk>/', views.RichiestaUpdateView.as_view(), name='review'),

]
