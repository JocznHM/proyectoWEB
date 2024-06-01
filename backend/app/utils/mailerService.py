"""
Este módulo se encarga de enviar correos electrónicos a los usuarios.
"""

# --------------------- IMPORTS --------------------- #
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from email_validator import validate_email, EmailNotValidError
from dotenv import load_dotenv
import os
load_dotenv()
# --------------------- VARIABLES ------------------- #
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_FROM = os.getenv("MAIL_FROM")
# --------------------- FUNCIONES ------------------- #
# Configuración de FastMail
conf = ConnectionConfig(
    MAIL_USERNAME=f"{MAIL_USERNAME}",
    MAIL_PASSWORD=f"{MAIL_PASSWORD}",
    MAIL_FROM=f"{MAIL_USERNAME}",
    MAIL_PORT=587,
    MAIL_SERVER=f"{MAIL_SERVER}",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
    )

# Instancia de FastMail para enviar correos
mail_sender = FastMail(conf)