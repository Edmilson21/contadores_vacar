from django.urls import path
from . import views 
              
app_name = "users_app"  
 
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register',), 
    path('login/', views.LoginUser.as_view(), name='user_login',), 
    path('logout/', views.LogoutView.as_view(), name='user_logout',), 
    path('update/', views.UpdatePasswordView.as_view(), name='user_update',), 
    path('user-verification/<pk>/', views.CodeVerificationView.as_view(), name='user-verification',), 
    path('usuarios/', views.UserListView.as_view(), name='usuarios',), 
    path('editar_usuarios/<pk>/', views.UserUpdateView.as_view(), name='editar_usuarios',), 
    path('eliminar_usuarios/<pk>/', views.UserDelete.as_view(), name='eliminar_usuarios',), 

]       
  
