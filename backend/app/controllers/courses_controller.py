"""
Este es el código del controlador de mi modelo courses
"""

#--------------- importaciones de librerías ---------------
import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
from typing import Dict, Any, List
from utils.database import db 
from utils.middleware import validate_bearer_token
from utils.global_functions import paginate

load_dotenv()

#-------------- variables globales-------------------
curso = APIRouter()
cursos_collection = db["courses"]
usuarios_collection = db["usuarios"]

#-------------- rutas del controlador ----------------


@curso.post("/crear_curso", response_description="Añadir nuevo curso")
async def crear_curso(data: dict, token: str = Depends(validate_bearer_token)):
    try:
        result = await cursos_collection.insert_one(data)
        creado_curso = await cursos_collection.find_one({"_id": result.inserted_id})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg": "Curso creado exitosamente"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@curso.get("/get_curso/{id}", response_description="Obtener un curso por ID")
async def obtener_curso(id: str, token: str = Depends(validate_bearer_token)):
    try:
        curso = await cursos_collection.find_one({"_id": ObjectId(id)})
        if curso is None:
            raise HTTPException(status_code=404, detail="Curso no encontrado")
        curso["_id"] = str(curso["_id"])
        return JSONResponse(status_code=status.HTTP_200_OK, content={"curso": curso})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@curso.put("/{id}", response_description="Actualizar un curso")
async def actualizar_curso(id: str, data: dict, token: str = Depends(validate_bearer_token)):
    try:
        result = await cursos_collection.update_one({"_id": id}, {"$set": data})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Curso no encontrado o datos sin cambios")
        actualizado_curso = await cursos_collection.find_one({"_id": id})
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "Curso actualizado exitosamente"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@curso.delete("/{id}", response_description="Eliminar un curso")
async def eliminar_curso(id: str, token: str = Depends(validate_bearer_token)):
    try:
        result = await cursos_collection.delete_one({"_id": id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Curso no encontrado")
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "Curso eliminado exitosamente"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@curso.get("/all_cursos", response_description="Obtener todos los cursos")
async def obtener_cursos(page: int = Query(1, gt=0), per_page: int = Query(10, gt=0), token: str = Depends(validate_bearer_token)):
    try:
        cursos = []
        async for curso in cursos_collection.find():
            curso["_id"] = str(curso["_id"])
            cursos.append(curso)
        total_items, total_pages, page, items_from_page = paginate(cursos, page, per_page)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"total_items": total_items, "total_pages": total_pages, "page": page, "cursos": items_from_page})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#cursos que son ofertas
@curso.get("/cursos_oferta", response_description="Obtener todos los cursos que son ofertas")
async def obtener_cursos_oferta(page: int = Query(1, gt=0), per_page: int = Query(10, gt=0), token: str = Depends(validate_bearer_token)):
    try:
        cursos = []
        async for curso in cursos_collection.find({"offer": True}):
            curso["_id"] = str(curso["_id"])
            cursos.append(curso)
        total_items, total_pages, page, items_from_page = paginate(cursos, page, per_page)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"total_items": total_items, "total_pages": total_pages, "page": page, "cursos": items_from_page})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@curso.post("/inscribir", response_description="Inscribirse a un curso")
async def inscribirse(data: dict, token: str = Depends(validate_bearer_token)):
    print(data)
    try:
        user = await usuarios_collection.find_one({"email": data["email"]})
        if user:
            # Verificar si 'courses' es un array, si no, convertirlo en un array vacío
            if not isinstance(user["courses"], list):
                await usuarios_collection.update_one({"_id": ObjectId(user["_id"])}, {"$set": {"courses": []}})
            # Agregar el curso al campo 'courses'
            print(user["courses"])
            if data["course_id"] not in user["courses"]:
                result = await usuarios_collection.update_one({"_id": ObjectId(user["_id"])}, {"$push": {"courses": data["course_id"]}})
                return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "Inscripción exitosa"})
            else:
                return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"msg": "Ya está inscrito en este curso"})
        else:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@curso.get("/mis_cursos/{email}", response_description="Obtener los cursos a los que está inscrito un usuario")
async def obtener_mis_cursos(email: str, token: str = Depends(validate_bearer_token)):
    try:
        user = await usuarios_collection.find_one({"email": email})
        if user:
            cursos = []
            for curso in user["courses"]:
                print(curso)
                curso_obj = await cursos_collection.find_one({"_id": ObjectId(curso)})
                curso_obj["_id"] = str(curso_obj["_id"])
                cursos.append(curso_obj)
                print(curso_obj)
            return JSONResponse(status_code=status.HTTP_200_OK, content={"cursos": cursos})
        else:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))