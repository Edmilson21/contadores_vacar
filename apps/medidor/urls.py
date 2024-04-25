from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (CruceView, VacarView,Mostrar_Empresas,CruceListView,VacarListView,
                    CruceUpdate,CruceDeleView,VacarUpdate,VacarDeleView,PanelControl,Panel_Control_Cruce,Panel_Control_Vacar)

urlpatterns = [
    path('entrar/', login_required(Mostrar_Empresas.as_view()), name='entrar'),
    path('cruce/', login_required(CruceView.as_view()), name='cruce'),
    path('vacar/', login_required(VacarView.as_view()), name='vacar'),
    path('cruce_list/', login_required(CruceListView.as_view()), name='cruce_list'),
    path('vacar_list/', login_required(VacarListView.as_view()), name='vacar_list'), 

    path('editar_cruce/<pk>/', login_required(CruceUpdate.as_view()), name='editar_cruce'),
    path('editar_vacar/<pk>/', login_required(VacarUpdate.as_view()), name='editar_vacar'),

    path('eliminar_cruce/<pk>/', login_required(CruceDeleView.as_view()), name='eliminar_cruce'),
    path('eliminar_vacar/<pk>/', login_required(VacarDeleView.as_view()), name='eliminar_vacar'),

    #Panel de Control
    path('panel_control/', login_required(PanelControl.as_view()), name='panel_control'),
    path('control_cruce/', login_required(Panel_Control_Cruce.as_view()), name='control_cruce'),
    path('control_vacar/', login_required(Panel_Control_Vacar.as_view()), name='control_vacar'),
    #path('correo/', enviar_correo, name='correo'), 
]      
         
  
   