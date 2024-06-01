"""
This file contains the middleware for the routes.
This middleware is used to validate the JWT token that is sent in the header of the request.
"""

# --------------------- IMPORTS --------------------- #
from typing import Optional
from fastapi import HTTPException, Header, Depends
from utils.jwt_utils import decode_token
import os
from dotenv import load_dotenv
from jwt import PyJWTError

# --------------------- VARIABLES ------------------- #
load_dotenv()

magic_word = os.getenv("SECRET_KEY")

# --------------------- FUNCIONES ------------------- #


async def validate_bearer_token(authorization: Optional[str] = Header(None)):
    try:
        if authorization is None:
            raise HTTPException(
                status_code=401, detail="Token no proporcionado en el encabezado")

        token_type, token = authorization.split()

        if token_type.lower() != "bearer":
            raise HTTPException(
                status_code=401, detail="Se esperaba un token Bearer")

        decoded_token = decode_token(token, magic_word)

        return decoded_token
    except PyJWTError as e:
        print(e)
        if "expired" in str(e):
            raise HTTPException(status_code=401, detail="Token ha expirado")
        else:
            raise HTTPException(
                status_code=401, detail="Token inválido o dañado")
