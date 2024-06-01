"""
    This Archivo contiene las funciones para generar y decodificar tokens.
"""
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()


magic_word = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")

def create_change_password_token(data: dict, expires_minutes: int):
    """
    Esta función genera un token para cambiar la contraseña, el cual contiene la información del usuario y la fecha de expiración.
    Recibe como parameetros un diccionario con la información del usuario y el tiempo de expiración.
    Retorna un token para cambiar la contraseña con la información del usuario y la fecha de expiración.
    """
    if expires_minutes == 0:
        expire = datetime.utcnow() + timedelta(minutes=5)
    else:
        expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode = data.copy()
    print()
    to_encode.update({"exp": expire})
    encoded_token = jwt.encode(to_encode, magic_word, algorithm=f"{algorithm}")
    return encoded_token

def create_token(data: dict):
    """
    Esta función genera un token de inicio de sesión, el cual contiene la información del usuario.
    recibe como parameetros un diccionario con la información del usuario.
    Retorna un token de inicio de sesión.
    """
    encoded_token = jwt.encode(data, magic_word, algorithm=f"{algorithm}")
    return encoded_token


"""
Esta función decodifica un token.
Recibe como parameetros un token y la contraseña secreta para decodificarlo.
Retorna el token decodificado que contiene datos del usuario y dependiendo del tipo de token, fecha de expiración.
"""
def decode_token(token, secret):
    return jwt.decode(token, secret, algorithms=['HS256'])
