from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('encuestas/', views.encuestas, name='encuestas'),
    path('crear_encuesta/', views.crear_encuesta, name='crear_encuesta'),
    path('llenar_encuesta/<int:encuesta_id>/', views.llenar_encuesta, name='llenar_encuesta'),
    path('lista_encuestas/', views.lista_encuestas, name='lista_encuestas'),
    path('gracias/', views.gracias, name='gracias'),
    path('encuesta/editar/<int:encuesta_id>/', views.editar_encuesta_form, name='editar_encuesta_form'),
    path('editar_encuesta/', views.editar_encuesta, name='editar_encuesta_list'),
    path('borrar_encuesta/<int:encuesta_id>/', views.borrar_encuesta, name='borrar_encuesta'),
    path('encuesta/<int:encuesta_id>/llenar/', views.compartir_encuesta, name='compartir_encuesta'),
    path('encuesta/<int:encuesta_id>/resultados/', views.resultados_encuesta, name='resultados_encuesta'),
    path('seleccionar_encuesta/', views.seleccionar_encuesta, name='seleccionar_encuesta'),
]
