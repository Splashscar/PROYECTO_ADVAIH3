from django.urls import path
from .views import EventoAPIView, EstadisticasAPIView
from .views_auth import RegistroAPIView, loginAPIView
from .views_perfil import PerfilImagenAPIView
from .views_perfil import subir_foto_perfil
from django.urls import path
from .views import EnviarTareasEmailAPIView
from .views_chat import ChatHistorialAPIView


urlpatterns = [
    path('auth/registro/', RegistroAPIView.as_view(), name='api_registro'),
    path('auth/login/', loginAPIView.as_view(), name='api_login'),
    # Primero la ruta de la lista/creación
    path('eventos/', EventoAPIView.as_view(), name='api_eventos'),

    # Luego la del detalle, y asegúrate de que termine en /
    path('eventos/<str:id>/', EventoAPIView.as_view(), name='api_evento_detalle'),
    #estadisticas

    path('eventos/estadisticas/', EstadisticasAPIView.as_view(), name='api_estadisticas'),
    path('perfil/foto/', PerfilImagenAPIView.as_view(), name='api_perfil_foto'),
    path('perfil/foto/', PerfilImagenAPIView.as_view(), name='api_perfil_foto'),
    #correo
    path('enviar-tareas/', EnviarTareasEmailAPIView.as_view()),
    path('chat/historial', ChatHistorialAPIView.as_view(), name='api_chat_historial')

]
