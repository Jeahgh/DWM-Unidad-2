# Tipos y utilidades de Python
from typing import List, Optional, Dict
from itertools import count

# FastAPI
from fastapi import FastAPI, HTTPException, Query

# Modelos y validación
from pydantic import BaseModel, Field

# MongoDB
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from contextlib import asynccontextmanager

# Para correr funciones async fuera de FastAPI
import asyncio


client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["bdGranJean"]
coll = db["items"]



app = FastAPI()



#crud con mongo

class Item(BaseModel):
    nombre: str
    precio: float
    descripcion: Optional[str] = None


@app.post("/items/")
async def crear_item(item: Item):
    resultado = await coll.insert_one(item.dict())
    return {"id": str(resultado.inserted_id)}


@app.get("/items/")
async def listar_items():
    items = []
    cursor = coll.find({})
    async for document in cursor:
        document["id"] = str(document["_id"])
        del document["_id"]
        items.append(document)
    return items


@app.get("/items/{item_id}")
async def obtener_item(item_id: str):
    document = await coll.find_one({"_id": ObjectId(item_id)})
    if document is None:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    document["id"] = str(document["_id"])
    del document["_id"]
    return document

@app.put("/items/{item_id}")
async def actualizar_item(item_id: str, item: Item):
    resultado = await coll.update_one({"_id": ObjectId(item_id)}, {"$set": item.dict()})
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return {"detail": "Item actualizado"}