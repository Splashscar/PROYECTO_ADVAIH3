from django.urls import path
from .views import EventoAPIView
from .views_auth import RegistroAPIView, loginAPIView
from .views_perfil import PerfilImagenAPIView

urlpatterns = [
    path('auth/registro/', RegistroAPIView.as_view(), name='api_registro'),
    path('auth/login/', loginAPIView.as_view(), name='api_eventos'),
    path('eventos/', EventoAPIView.as_view(), name='api_eventos'),
    path('eventos/<str:id>', EventoAPIView.as_view(), name='api_evento_detalle'),
    path('perfil/foto/', PerfilImagenAPIView.as_view(), name='api_perfil_foto'),

]