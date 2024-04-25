from django import forms
from .models import Empresa,Cruce,Vacar



class SelectEmpresa(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre_empresa']

    def __init__(self, *args, **kwargs):
        super(SelectEmpresa, self).__init__(*args, **kwargs)
        self.fields['nombre_empresa'].widget = forms.Select(attrs={'class': 'select-box'})
        self.fields['nombre_empresa'].choices = [(empresa.id, empresa.nombre_empresa) for empresa in Empresa.objects.all()]
 

class CruceForm(forms.ModelForm): 
    class Meta: 
        model = Cruce
        fields = ['valor_agua', 'agua1', 'agua2', 'bombero', 'valor_luz', 'valor_gas', 'fecha_registro', 'empresa']
     
        widgets = { 
            'fecha_registro': forms.DateInput(attrs={'type': 'date'}),
        }


    def __init__(self, *args, **kwargs):
        # Obtener la empresa seleccionada del argumento inicial (si existe)
        empresa_seleccionada = kwargs.pop('empresa_seleccionada', None)
        super().__init__(*args, **kwargs)
        # Establecer la empresa seleccionada como valor inicial del campo empresa
        if empresa_seleccionada:
            self.fields['empresa'].initial = empresa_seleccionada

 

   
class VacarForm(forms.ModelForm):
    class Meta:
        model = Vacar
        fields = ['valor_agua', 'valor_P1', 'valor_P2', 'valor_P3', 'valor_gas_derecho', 'valor_gas_izquierdo', 'valor_gas_casa', 'gas', 'fecha_registro', 'fecha_registro', 'empresa']

        widgets = {
            'fecha_registro': forms.DateInput(attrs={'type': 'date'}),
        }  
        

    def clean_valor_gas_casa(self):
        valor_gas_casa = self.cleaned_data.get('valor_gas_casa')

        if not (0 <= valor_gas_casa <= 95):
            raise forms.ValidationError("El valor del Gás(Casa) debe estar en el rango de 0 a 95.")

        return valor_gas_casa

    
    def __init__(self, *args, **kwargs): 
        # Obtener la empresa seleccionada del argumento inicial (si existe)
        empresa_seleccionada = kwargs.pop('empresa_seleccionada', None)
        super().__init__(*args, **kwargs)
        # Establecer la empresa seleccionada como valor inicial del campo empresa
        if empresa_seleccionada:
            self.fields['empresa'].initial = empresa_seleccionada

 
 
#Formularios para o Painel de Control
    
class VacarFormPanel(forms.ModelForm):
    class Meta:
        model = Vacar
        fields = ['valor_agua', 'valor_P1', 'valor_P2', 'valor_P3', 'valor_gas_derecho', 'valor_gas_izquierdo', 'valor_gas_casa', 'gas', 'fecha_registro', 'fecha_registro', 'empresa']

        widgets = {
            'fecha_registro': forms.DateInput(attrs={'type': 'date'}),
        } 
    

    def clean_valor_gas_casa(self):
        valor_gas_casa = self.cleaned_data.get('valor_gas_casa')

        if not (0 <= valor_gas_casa <= 95):
            raise forms.ValidationError("El valor del Gás(Casa) debe estar en el rango de 0 a 95.")

        return valor_gas_casa
    




class CruceFormPanel(forms.ModelForm):
    class Meta:
        model = Cruce
        fields = ['valor_agua', 'agua1', 'agua2', 'bombero', 'valor_luz', 'valor_gas', 'fecha_registro', 'empresa']

        widgets = {
            'fecha_registro': forms.DateInput(attrs={'type': 'date'}),
        }

