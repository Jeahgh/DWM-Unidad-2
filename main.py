from typing import List, Optional, Dict
from itertools import count



from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Mi Primera API", version="1.0.0")


@app.get("/")
def read_root():
    return {"message": "que pasa mi gente"}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id, 
            "nombre": f"Producto {item_id}"
    }

@app.get("/hello/{username}")
def greet_user(username: str):
    return{
        "saludo": f"Hola, {username}! bienvenido a mi API"
    }

@app.get("/search/")
def search(q:str, max_results:int=10):
    return{
        "query": q,
        "max_results": max_results
    }



#simular base de datos
mi_db ={}
id_counter = count(1)



## Request body
#validaciones



@app.get("/users/")
def listar_users():
    return[{
        "id": user_id,
        "user": user
    } for user_id, user in mi_db.items()
    ]




#CRUD

class User(BaseModel):
    username: str = Field(min_length=3, max_length=50, description="Nombre de usuario")
    age: int = Field(gt=0, lt=150, description="Edad del usuario")

@app.post("/users/")
def crear_user(user: User):
    user_id = next(id_counter)
    mi_db[user_id] = user
    return{
        "id": user_id,
        "user": user.model_dump()
    }

@app.get("/users/{user_id}")
def obtener_user(user_id: int):
    if user_id not in mi_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return{
        "id": user_id,
        "user": mi_db[user_id].model_dump()
    }

@app.put("/users/{user_id}")
def actualizar_user(user_id: int, user: User):
    if user_id not in mi_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    mi_db[user_id] = user
    return{
        "id": user_id,
        "user": user.model_dump()
    }

@app.delete("/users/{user_id}")
def eliminar_user(user_id: int):
    if user_id not in mi_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    del mi_db[user_id]
    return{
        "detail": "Usuario eliminado"
    }





