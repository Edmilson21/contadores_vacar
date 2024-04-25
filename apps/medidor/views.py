from django.db.models.query import QuerySet
from django.views import View
from django.shortcuts import render, redirect
from .forms import SelectEmpresa,CruceForm,VacarForm,VacarFormPanel,CruceFormPanel
from django.urls import reverse_lazy
from .models import Cruce,Vacar,Empresa
from django.views.generic.edit import CreateView
from django.views.generic import (ListView,CreateView,TemplateView,DetailView,UpdateView,DeleteView)
from django.utils import timezone
from datetime import datetime
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect




# Create your views here.  
 
class Mostrar_Empresas(View):
    template_name = 'SelectEmpresa.html'  

    def get(self, request, *args, **kwargs):
        empresas = Empresa.objects.all()
        return render(request, self.template_name, {'empresas': empresas})

    def post(self, request, *args, **kwargs):
        empresa_id = request.POST.get('nombre_empresa')
        
        if empresa_id:
            empresa = Empresa.objects.get(pk=empresa_id)
            if empresa.nombre_empresa == 'El Cruce de Villaharta':
                return redirect('cruce')
            elif empresa.nombre_empresa == 'El Vacar':
                return redirect('vacar')
         
        empresas = Empresa.objects.all() 
        return render(request, self.template_name, {'empresas': empresas})




class CruceView(CreateView): 
    template_name = 'formularios_cruce.html'
    form_class = CruceForm
    model = Cruce
    success_url = reverse_lazy('cruce_list')  
 
 # Saving the date and ssuccessfull mesage.
    def form_valid(self, form):
        form.instance.fecha_registro = timezone.now().date() 
        messages.success(self.request, 'Guardado con éxito')  
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empresa_seleccionada = Empresa.objects.all()[0]  # Aquí selecciona la segunda empresa, asegúrate de que sea la deseada
        print("€€€€€€€€€€€€ Empresa Seleccionada:",empresa_seleccionada)
        context['empresa_seleccionada'] = empresa_seleccionada
        print("Contexto:",context)
        return context



class VacarView(CreateView): 
    template_name = 'formularios_vacar.html'
    form_class = VacarForm 
    model = Vacar  
    success_url = reverse_lazy('vacar_list')   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empresa_seleccionada = Empresa.objects.all()[1]
        context['empresa_seleccionada'] = empresa_seleccionada
        context['form_vacar'] = self.get_form()
        return context

    def form_valid(self, form):
        try:
            ultimo_valor_gas_casa = Vacar.objects.latest('fecha_registro').valor_gas_casa
        except Vacar.DoesNotExist:
            # Si la base de datos está vacía, permitir que el valor ingresado se guarde de forma normal
            return super().form_valid(form)

        valor_ingresado = form.cleaned_data['valor_gas_casa']

        if valor_ingresado <= ultimo_valor_gas_casa:
            # Si el valor ingresado es menor o igual al último valor registrado, guardar los datos en la base de datos
            messages.success(self.request, '¡Guardado exitosamente!')
            return super().form_valid(form)
        else:
            # Si el valor ingresado es mayor que el último valor registrado, mostrar un mensaje de error
            messages.error(self.request, 'El valor ingresado en el campo Gas(Casa) debe ser menor o igual al último valor registrado.')
            self.request.error = 'El valor ingresado en el campo Gas(Casa) debe ser menor o igual al último valor registrado.'
            return self.form_invalid(form)

 
    

# Listar los datos para El Cruce
    
class CruceListView(ListView):
    model = Cruce
    template_name = 'cruce_list.html'
    context_object_name = 'cruces'
    paginate_by = 4

    # Finding the date 

    def get_queryset(self):
        fecha = self.request.GET.get("kword", '')

        if not fecha:
            # Si no se proporciona ninguna fecha, mostrar todos los registros
            return Cruce.objects.all()

        try:
            fecha_obj = datetime.strptime(fecha, '%d-%m-%Y').date()
        except ValueError:
            try:
                fecha_obj = datetime.strptime(fecha, '%d/%m/%Y').date()
            except ValueError:
                try:
                    fecha_obj = datetime.strptime(fecha, '%d-%m-%y').date()
                except ValueError:
                    try:
                        fecha_obj = datetime.strptime(fecha, '%d/%m/%y').date()
                    except ValueError:
                        # Manejo de error si todos los formatos fallan
                        return Cruce.objects.none()

        return Cruce.objects.filter(fecha_registro=fecha_obj)



# Listar los datos Vacar

class VacarListView(ListView):
    model = Vacar
    template_name = 'vacar_list.html'
    context_object_name = 'vacars'
    paginate_by = 4  # Paginación

 
    def get_queryset(self):
        fecha = self.request.GET.get("kword", '')

        if not fecha:
            # Si no se proporciona ninguna fecha, mostrar todos los registros
            return Vacar.objects.all()

        try:
            fecha_obj = datetime.strptime(fecha, '%d-%m-%Y').date()
        except ValueError:
            try:
                fecha_obj = datetime.strptime(fecha, '%d/%m/%Y').date()
            except ValueError:
                try:
                    fecha_obj = datetime.strptime(fecha, '%d-%m-%y').date()
                except ValueError:
                    try:
                        fecha_obj = datetime.strptime(fecha, '%d/%m/%y').date()
                    except ValueError:
                        # Manejo de error si todos los formatos fallan
                        return Vacar.objects.none()

        return Vacar.objects.filter(fecha_registro=fecha_obj)
 
    
#----------------------------------------- 
       
# Actualizar El Cruce
    
class CruceUpdate(UpdateView):
    template_name = 'update_cruce.html'
    model = Cruce
    form_class = CruceForm
    #fields = ['valor_agua','agua1','agua2','bombero','valor_luz','valor_gas','fecha_registro']
    success_url = reverse_lazy('cruce_list')  

    def form_valid(self, form):
        response = super().form_valid(form)
        # Configura el mensaje de éxito
        messages.success(self.request, 'Actualizado con éxito')
        return response
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empresa_seleccionada = Empresa.objects.all()[0]  # Aquí selecciona la segunda empresa, asegúrate de que sea la deseada
        context['empresa_seleccionada'] = empresa_seleccionada
        return context


# Eliminar El Cruce 

class CruceDeleView(DeleteView):
    model = Cruce 
    template_name = "delete_cruce.html"
    success_url = reverse_lazy('cruce_list')  # Página para redireccionar cuando se borra el dato
    context_object_name = 'object'

    def delete(self, request, *args, **kwargs):
        # Elimina el objeto
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        # Configura el mensaje de éxito
        messages.success(self.request, 'Eliminado con éxito')
        return HttpResponseRedirect(success_url)

# Actualizar El Vacar 
    
class VacarUpdate(UpdateView):
    template_name = 'update_vacar.html'
    model = Vacar
    form_class = VacarForm  
    #fields = ['valor_agua', 'valor_P1', 'valor_P2', 'valor_P3', 'valor_gas_derecho', 'valor_gas_izquierdo', 'valor_gas_casa', 'gas', 'fecha_registro', 'empresa']
    success_url = reverse_lazy('vacar_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Configura el mensaje de éxito
        messages.success(self.request, 'Actualizado con éxito')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empresa_seleccionada = Empresa.objects.all()[1]  # Aquí selecciona la segunda empresa, asegúrate de que sea la deseada
        context['empresa_seleccionada'] = empresa_seleccionada
        return context
    

# Eliminar El Vacar
     
class VacarDeleView(DeleteView):
    model = Vacar
    template_name = "delete_vacar.html"
    context_object_name = 'object'
    success_url = reverse_lazy('vacar_list')

    def delete(self, request, *args, **kwargs):
        # Elimina el objeto
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        # Configura el mensaje de éxito
        messages.success(self.request, 'Eliminado con éxito')
        return HttpResponseRedirect(success_url)




# Panel de Control General

class PanelControl(TemplateView):
    template_name = 'panel_control.html'
    context_object_name = 'panel'

  
    
#Panel de Control Vacar
    
class Panel_Control_Vacar(CreateView):
    
    model = Vacar
    template_name = 'Panel_vacar.html'
    form_class = VacarFormPanel
    context_object_name = 'vac'
    success_url = reverse_lazy('vacar_list')  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empresa_seleccionada = Empresa.objects.all()[1]  # Aquí selecciona la segunda empresa, asegúrate de que sea la deseada
        context['empresa_seleccionada'] = empresa_seleccionada
        context['form_panel'] = self.get_form()        
        return context
    
    
    def form_valid(self, form):
        # Llama al método form_valid() de la superclase para realizar las operaciones predeterminadas
        response = super().form_valid(form)
    
        # Configura el mensaje de éxito 
        messages.success(self.request, 'Guardado con éxito')
    
        # Obtiene el valor ingresado del formulario
        valor_ingresado = form.cleaned_data['valor_gas_casa']
    
        # Configura los detalles del correo  
        subject = 'APP Vacar'
        message = "Hola, soy la App del Vacar, te informo que se ha rellenado el gas en un valor de: {} %.\n ***Saludos***!".format(valor_ingresado)  
        from_email = 'mdrvacar@gmail.com'  
        recipient_list = ['administracion@elvacar.es'] 
        #recipient_list = ['carlosnascimento210594@gmail.com']  
        
    
        # Envía el correo electrónico
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    
        # Devuelve la respuesta
        return response
    
    
        
    


#Panel de Control Cruce

class Panel_Control_Cruce(CreateView):
    model = Cruce
    template_name = 'Panel_cruce.html'
    form_class = CruceFormPanel
    context_object_name = 'cruc'
    success_url = reverse_lazy('cruce_list')  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()  # Renderiza el formulario CruceFormPanel
        return context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empresa_seleccionada = Empresa.objects.all()[0]  # Aquí selecciona la segunda empresa, asegúrate de que sea la deseada
        context['empresa_seleccionada'] = empresa_seleccionada
        return context











''' 
# Part to send Email from the APP
    
def enviar_correo(request):
    # Configura los detalles del correo
    subject = 'APP Vacar'
    message = " Hola, soy la App del Vacar, te lo envio este mensaje como forma de testeo.\n ***Saludos***!"  
      
    from_email = 'mdrvacar@gmail.com'  # Reemplaza con tu dirección de correo
    recipient_list = ['edmilsoncarlosn94@gmail.com']  # Reemplaza con la dirección de correo del destinatario

    # Envia el correo
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    return render(request, 'correo_enviado.html')

'''