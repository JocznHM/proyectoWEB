""" 
Este archivo guarda las funciones para validar expresiones regulares y otros tipos de validaciones
"""
#--------------- importaciones de librerias ---------------
import re

#-------------- funciones globales ----------------
def validate_email(email: str):
    """
    Valida si el email tiene el formato correcto
    Recibe como parametro el email a validar
    retorna True si el email es valido, False si no lo es
    """
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))


def validate_password(password: str):
    """
    Valida si la contraseña tiene al menos 8 caracteres, una letra mayúscula, una letra minúscula, un símbolo y un número.
    Recibe como parámetro la contraseña a validar
    Retorna True si la contraseña es válida, False si no lo es
    """
    return bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?#&])[A-Za-z\d@$!%*?#&]{8,}$", password))
