# Funciones Extras.
 
import random
import string

# Función Generar Codigo

def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))