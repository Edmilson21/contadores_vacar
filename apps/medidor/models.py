from django.db import models

# Create your models here.
 
class Empresa(models.Model):
    nombre_empresa = models.CharField("Empresa", max_length=100, unique=True)  # Cambié max_length a un valor más grande para admitir nombres más largos

    def __str__(self):
        return self.nombre_empresa
 

class Cruce(models.Model): 
    valor_agua = models.IntegerField()
    agua1 = models.IntegerField()
    agua2 = models.IntegerField() 
    bombero = models.IntegerField()
    valor_luz = models.IntegerField()
    valor_gas = models.IntegerField()
    #fecha_registro = models.DateTimeField('Fecha de Registro', auto_now_add=True)
    fecha_registro = models.DateField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)

 
class Vacar(models.Model): 
    valor_agua = models.IntegerField() 
    valor_P1 = models.IntegerField() 
    valor_P2 = models.IntegerField()
    valor_P3 = models.IntegerField()
    valor_gas_derecho = models.IntegerField()
    valor_gas_izquierdo = models.IntegerField()
    valor_gas_casa = models.IntegerField()
    gas = models.IntegerField()
    fecha_registro = models.DateField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)


