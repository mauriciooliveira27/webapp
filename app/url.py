from django.urls import path, include
from django.urls import reverse

from .views import (ListPlacaView,ConfigurePlacaView,
                    UpdateCordoesView,UpdatePlacaView,
                    DeletePlacaView,ListCordoesView,
                    DeleteCordaoView,CreateCordaoView,
                    SensorConfigView,ServicosView,ServicosStopView,
                    ServicosStatusView,AsyncClassView)



urlpatterns = [
    path('home/',ListPlacaView.as_view(), name='home'),
    path('configuracao-placa/',ConfigurePlacaView.as_view(), name='configuracao-placa'),
    path('update-cordoes/', UpdateCordoesView.as_view(), name='update-cordoes'),
    path('<int:pk>/update-placa/',UpdatePlacaView.as_view(), name= 'update-placa'),
    path('<int:pk>/delete-placa/',DeletePlacaView.as_view(), name= 'delete-placa'),
    path('list-cordoes/',ListCordoesView.as_view(), name= 'list-cordoes'),
    path('<int:pk>/delete-cordao/',DeleteCordaoView.as_view(), name='delete-cordao' ),
    path('cadastrar-cordao/',CreateCordaoView.as_view(), name='cadastrar-cordoes' ),
    path('configurar/', SensorConfigView.as_view(), name='sensor_config_form'),
    path('servicos/', ServicosView.as_view(), name='servico-start'),
    path('servicos-stop/', ServicosStopView.as_view(), name='servico-stop'),
    path('servicos-status/', ServicosStatusView.as_view(), name='servico-status'),
    path('async-class-view/', AsyncClassView.as_view(), name='async_class_view'),
    
]

