from pydantic import BaseModel

class UsuarioModel(BaseModel):
    nombre_completo: str
    email: str
    password: str
