from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.usuario_controller import usuario as usuario_router
from controllers.courses_controller import curso as curso_router

app = FastAPI(
    title="InventarioAPI",
    description="API para el sistema de inventarios",
    version="1.0 indev"
)


origins = [
    "http://localhost:5000",
    "http://127.0.0.1:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(usuario_router, prefix="/usuarios")
app.include_router(curso_router, prefix="/cursos")