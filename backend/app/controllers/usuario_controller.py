
"""
Este es el codigo del controlador de mi modelo UsuarioModel
"""

#--------------- importaciones de librerias ---------------
import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi_mail import MessageSchema, MessageType
from pydantic import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from models.usuario_model import UsuarioModel
from utils.database import db 
from utils.middleware import validate_bearer_token
from utils.jwt_utils import create_change_password_token, decode_token, create_token
from utils.validate import validate_email, validate_password
import re
from utils.mailerService import mail_sender

load_dotenv()

#-------------- variables globales-------------------
usuario = APIRouter()
usuarios_collection = db["usuarios"]
MAIL_FROM = os.getenv("MAIL_FROM")

#-------------- funciones globales ----------------

#-------------- rutas del controlador ----------------
@usuario.post("/sign_in")
async def sign_in(userdata: dict):
    """
    Ruta para iniciar sesion
    recibe como parametros el usuario y la contraseña
    Retorna un token de inicio de sesión
    """
    if userdata is None:
        return JSONResponse(content={"error": "No se han enviado datos"}, status_code=status.HTTP_400_BAD_REQUEST)
    
    if userdata == {}:
        return JSONResponse(content={"error": "El json recibido esta vacio"}, status_code=status.HTTP_400_BAD_REQUEST)
    email_user = userdata["email"]
    password_user = userdata["password"]
    
    if email_user == "" or password_user == "":
        return JSONResponse(content={"error": "El email y la contraseña son obligatorios"}, status_code=status.HTTP_400_BAD_REQUEST)
    
    if not validate_email(email_user):
        return JSONResponse(content={"error": "El email no cumple la sintaxis de un email"}, status_code=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = await usuarios_collection.find_one({"email": email_user})
        if user:
            if check_password_hash(user["password"], password_user):
                payload = {
                    "email": user["email"],
                    "nombre_completo": user["nombre_completo"]
                }

                token = create_token(payload)
                return JSONResponse(content={"success": "Inicio de sesión exitoso", "token": token}, status_code=status.HTTP_200_OK)
            else:
                return JSONResponse(content={"error": "contraseña incorrecta"}, status_code=status.HTTP_400_BAD_REQUEST)
        else:
            return JSONResponse(content={"error": "email no encontrado en la bd"}, status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print (e)
        return JSONResponse(content={"error": "Error en el servidor", "error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@usuario.post("/sign_up")
async def sign_up(userdata: dict):
    """
    Ruta para registrar un nuevo usuario
    Recibe como parametros el nombre, email y contraseña
    Retorna un mensaje de confirmación
    """
    
    if userdata is None:
        return JSONResponse(content={"error": "No se han enviado datos"}, status_code=status.HTTP_400_BAD_REQUEST)
    
    if userdata == {}:
        return JSONResponse(content={"error": "El json recibido esta vacio"}, status_code=status.HTTP_400_BAD_REQUEST)
    try:
        user_data_model = UsuarioModel(**userdata)
        if user_data_model:
            for key, value in userdata.items():
                if value == "":
                    return JSONResponse(content={"error": f"El campo '{key}' es obligatorio"}, status_code=status.HTTP_400_BAD_REQUEST)

            if not validate_email(userdata["email"]) or not validate_password(userdata["password"]):
                return JSONResponse(content={"error": "El email o la contraseña no cumplen la validación"}, status_code=status.HTTP_400_BAD_REQUEST)
            
            try:
                if await usuarios_collection.find_one({"email": userdata["email"]}):
                    return JSONResponse(content={"error": "El email ya se encuentra registrado"}, status_code=status.HTTP_400_BAD_REQUEST)
                hashed_password = generate_password_hash(userdata["password"])
                userdata["password"] = hashed_password
                user = await usuarios_collection.insert_one(userdata)
                return JSONResponse(content={"success": "Usuario registrado correctamente"}, status_code=status.HTTP_201_CREATED)
            except Exception as e:
                return JSONResponse(content={"error": "Error en el servidor", "error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return JSONResponse(content={"error": "El JSON recibido no coincide con el modelo"}, status_code=status.HTTP_400_BAD_REQUEST)
    except ValidationError as e:
        return JSONResponse(content={"error": "Error de validación de datos", "error": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JSONResponse(content={"error": "Error en el servidor", "error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@usuario.get("/get_user/email={email}")
async def get_user(email: str, token: str = Depends(validate_bearer_token)):
    """
    Ruta para obtener un usuario
    Recibe como parametro el email del usuario
    Retorna la información del usuario
    """
    if email == "":
        return JSONResponse(content={"error": "El email es obligatorio"}, status_code=status.HTTP_400_BAD_REQUEST)
    if email is None:
        return JSONResponse(content={"error": "No se ha enviado el email"}, status_code=status.HTTP_400_BAD_REQUEST)
    if not validate_email(email):
        return JSONResponse(content={"error": "El email no cumple la validación"}, status_code=status.HTTP_400_BAD_REQUEST)
    try:
        user = await usuarios_collection.find_one({"email": email})
        if user:
            user["_id"] = str(user["_id"])
            user.pop("password")
            return JSONResponse(content={"data_user":user}, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"error": "Usuario no encontrado"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse(content={"error": "Error en el servidor", "error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@usuario.put("/update_user")
async def update_user(userdata: dict, token: str = Depends(validate_bearer_token)):
    """
    Ruta para actualizar un usuario
    Recibe como parametros los campos a actualizar
    Retorna un mensaje de confirmación
    """
    for key, value in userdata.items():
        if value == "":
            return JSONResponse(content={"error": f"El campo '{key}' es obligatorio"}, status_code=status.HTTP_400_BAD_REQUEST)
    
    if not validate_email(userdata["email"]):
                return JSONResponse(content={"error": "El email no cumple la validación"}, status_code=status.HTTP_400_BAD_REQUEST)
    try:
        user = await usuarios_collection.find_one({"email": userdata["email"]})
        if user:
            res = await usuarios_collection.update_one({"email": userdata["email"]}, {"$set": userdata})
            return JSONResponse(content={"message": "Usuario actualizado correctamente"}, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"error": "Usuario no encontrado"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse(content={"error": "Error en el servidor", "error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@usuario.delete("/delete_user/email={email}")
async def delete_user(email: str, token: str = Depends(validate_bearer_token)):
    """
    Ruta para eliminar un usuario
    Recibe como parametro el email del usuario
    Retorna un mensaje de confirmación
    """
    if email == "":
        return JSONResponse(content={"error": "El email es obligatorio"}, status_code=status.HTTP_400_BAD_REQUEST)
    if email is None:
        return JSONResponse(content={"error": "No se ha enviado el email"}, status_code=status.HTTP_400_BAD_REQUEST)
    if not validate_email(email):
        return JSONResponse(content={"error": "El email no cumple la validación"}, status_code=status.HTTP_400_BAD_REQUEST)
    try:
        user = await usuarios_collection.find_one({"email": email})
        if user:
            res = await usuarios_collection.delete_one({"email": email})
            return JSONResponse(content={"message": "Usuario eliminado"}, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"error": "Usuario no encontrado"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse(content={"error": "Error en el servidor", "error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@usuario.get("/get_all_users")
async def get_all_users(token: str = Depends(validate_bearer_token)):
    """
    Ruta para obtener todos los usuarios
    Retorna una lista con la información de todos los usuarios
    """
    try:
        users = []
        async for user in usuarios_collection.find():
            user["_id"] = str(user["_id"])
            user.pop("password")
            users.append(user)
        return JSONResponse(content={"data_users": users}, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(content={"error": "Error en el servidor", "error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@usuario.post("/set_password")
async def set_password(userdata:dict, token: str = Depends(validate_bearer_token)):
    """
    Ruta para cambiar la contraseña de un usuario
    Recibe como parametros el email del usuario y la nueva contraseña
    Retorna un mensaje de confirmación
    """
    if userdata is None:
        return JSONResponse(content={"error": "No se han enviado datos"}, status_code=status.HTTP_400_BAD_REQUEST)
    if userdata == {}:
        return JSONResponse(content={"error": "El json recibido esta vacio"}, status_code=status.HTTP_400_BAD_REQUEST)
    
    for key, value in userdata.items():
        if value == "":
            return JSONResponse(content={"error": f"El campo '{key}' es obligatorio"}, status_code=status.HTTP_400_BAD_REQUEST)

    if not validate_email(userdata["email"]) or not validate_password(userdata["password"]):
        return JSONResponse(content={"error": "La contraseña no cumple con la validación"}, status_code=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = await usuarios_collection.find_one({"email": userdata["email"]})
        if user:
            hashed_password = generate_password_hash(userdata["password"])
            res = await usuarios_collection.update_one({"email": userdata["email"]}, {"$set": {"password": hashed_password}})
            return JSONResponse(content={"message": "Contraseña actualizada correctamente"}, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"error": "Usuario no encontrado"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse(content={"error": "Error en el servidor", "error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@usuario.post("/generate_token_password")
async def generate_token_password(data: dict):
    """
    Genera un token para restablecer la contraseña de un usuario y la envia por correo electrónico.
    Recibe como parametro el correo electrónico del usuario.
    Retorna un objeto de respuesta JSON que contiene un mensaje de éxito o un mensaje de error,
    junto con el código de estado correspondiente y el tiempo de expiración del token.
    """
    email = data.get("email")
    try:
        "#regex para validar el correo electrónico"
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return JSONResponse(content={"error": "El correo electrónico no es válido."}, status_code=status.HTTP_400_BAD_REQUEST)
        
        user = await usuarios_collection.find_one({"email": email})
        if not user:
            return JSONResponse(content={"error": "El usuario no existe."}, status_code=status.HTTP_401_UNAUTHORIZED)
        elif user["status"] == "inactive":
            return JSONResponse(content={"error": "El usuario no está activo."}, status_code=status.HTTP_401_UNAUTHORIZED)
        user_role = user["role"]
        payload = {
            "email": user["email"],
            "fullname": user["fullname"],
            "role": user_role
        }
        expire_time = 5
        token = create_change_password_token(
            payload, expires_minutes=expire_time)
        
        """
        Se crea el mensaje que se enviará por correo electrónico
        para esto se utiliza el objeto MessageSchema de fastapi_mail
        """
        body_mail = f"""
            <html>
            <head>
                <title>Recuperación de Cuenta</title>
            </head>
            <body>
                <p>Hola {user["fullname"]},</p>
                <p>Se ha solicitado restablecer tu contraseña de Think Unlimited. 
                Usa el siguiente token para completar el proceso de recuperación de cuenta:</p>
                <p><strong>{token}</strong></p>
                <p>Recuerda que este token expirará en {expire_time} minutos.</p>
                <p>Si no has solicitado este restablecimiento, puedes ignorar este correo.</p>
                <p>Gracias, <br> {MAIL_FROM}</p>
            </body>
            </html>
        """
        message = MessageSchema(
            subject="Restablecer contraseña Think Unlimited",
            recipients=[email],
            body=body_mail,
            subtype=MessageType.html
        )

        # Se envía el correo electrónico
        await mail_sender.send_message(message)
        return JSONResponse(content={"sended": True, "time_expire_min":expire_time}, status_code=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return JSONResponse(content={"error": "Error interno del servidor"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)