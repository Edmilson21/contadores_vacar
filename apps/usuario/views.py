from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    View, ListView, UpdateView, DeleteView
)
from django.views.generic.edit import (
    FormView
)

from .forms import (UserRegisterForm, LoginForm,
                    UpdatePasswordForm, VerificationForm, UserUpdateForm)
from .functions import code_generator
from .models import User
 

# Create your views here.


class UserRegisterView(FormView):
    template_name = 'usuario/register.html'
    form_class = UserRegisterForm
    success_url = '/' 

    def form_valid(self, form):
        # Generando el Codigo
        codigo = code_generator()


        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres = form.cleaned_data['nombres'],
            apellidos = form.cleaned_data['apellidos'],
            genero = form.cleaned_data['genero'],
            codregistro = codigo

        )

        # Enviar el codigo al email del usuario
        asunto = 'Confirmación de Email'
        mensaje = 'Código de Verificación: ' + codigo
        email_remitente = 'mdrvacar@gmail.com'

        send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email'],])
        # Redirigir a pantalla de verificación.
        return HttpResponseRedirect(
            reverse(
                'users_app:user-verification',
                kwargs={'pk': usuario.id}
            )
        )


class LoginUser(FormView):
    template_name = "usuario/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('entrar')

    def form_valid(self, form): 
        # Verificar el LOGIN
        user= authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password']
        )
        # Haciendo el Login
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)


class LogoutView(View):

    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user_login'
            )
    )


class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = "usuario/update.html"
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user_login')
    login_url = reverse_lazy('users_app:user_login')

    def form_valid(self, form):
        usuario = self.request.user
        user= authenticate(
            username = usuario.username,
            password = form.cleaned_data['password1']
        )

        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()

        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)




class CodeVerificationView(FormView):
    template_name = "usuario/verification.html"
    form_class = VerificationForm
    success_url = reverse_lazy('users_app:user_login')

    def get_form_kwargs(self):
        kwargs = super(CodeVerificationView, self).get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs['pk'],
        })
        return kwargs

    def form_valid(self, form):
        User.objects.filter(
            id=self.kwargs['pk']
        ).update(
            is_active = True
        )
       
       
        return super(CodeVerificationView, self).form_valid(form)


# Usuarios

class UserListView(ListView):
    model = User
    template_name = 'usuario/user_list.html'
    context_object_name = 'usuarios'
    paginate_by = 7 # Paginación


  
class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'usuario/user_update.html'
    success_url = reverse_lazy('users_app:usuarios')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Configura el mensaje de éxito
        messages.success(self.request, 'Actualizado con éxito')
        return response



class UserDelete(DeleteView):
    model = User
    template_name = "usuario/delete_user.html"
    context_object_name = 'object'
    success_url = reverse_lazy('users_app:usuarios')

    def delete(self, request, *args, **kwargs):
        # Elimina el objeto
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        # Configura el mensaje de éxito
        messages.success(self.request, 'Eliminado con éxito')
        return HttpResponseRedirect(success_url)
    






   

    
