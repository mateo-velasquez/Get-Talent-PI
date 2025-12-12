from fastapi import FastAPI, HTTPException
from typing import List
from schema import Task, TaskUpdate

app = FastAPI(title="Get Talent: Gestor de Tareas API", version="1.0.0")

# --- BASE DE DATOS EN MEMORIA ---
TASK_DB: List[dict] = [
    {
        "id": 1,
        "title": "Configurar Entorno de Desarrollo",
        "description": "Instalar Python, FastAPI, Uvicorn y configurar el IDE.",
        "completed": False,
        "priority": 5,
        "due_date": "2025-12-15T10:00:00Z",
        "category": "Trabajo",
        "subtasks": [
            {"id": 101, "title": "Instalar dependencias con pip", "completed": True},
            {"id": 102, "title": "Crear proyecto base de FastAPI", "completed": False}
        ]
    },
    {
        "id": 2,
        "title": "Preparar Cena Familiar",
        "description": "Comprar ingredientes y cocinar lasaña para la reunión del domingo.",
        "completed": True,
        "priority": 3,
        "due_date": "2025-12-14T18:30:00Z",
        "category": "Personal",
        "subtasks": [
            {"id": 201, "title": "Ir al supermercado", "completed": True},
            {"id": 202, "title": "Cocinar el plato principal", "completed": True},
            {"id": 203, "title": "Poner la mesa", "completed": True}
        ]
    }
]


# Endpoints
@app.get("/tasks", response_model=List[Task])
def get_all_tasks():
    return TASK_DB

@app.get("/tasks/{task_id}", response_model=Task)
def get_task_by_id(task_id: int):
    task = list(filter(lambda x: x['id'] == task_id, TASK_DB))
    if len(task) > 0:
        return task[0]
    raise HTTPException(status_code=404, detail='Tarea no encontrada')

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: Task):
    if TASK_DB:
        new_id = max(t["id"] for t in TASK_DB) + 1
    else:
        new_id = 1

    task_dict = task.model_dump()
    task_dict["id"] = new_id
    
    TASK_DB.append(task_dict)
    return task_dict

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(TASK_DB):
        if task["id"] == task_id:
            task_data = updated_task.model_dump()
            task_data["id"] = task_id 
            
            TASK_DB[index] = task_data
            return task_data
            
    raise HTTPException(status_code=404, detail="Tarea no encontrada para actualizar")

@app.patch("/tasks/{task_id}", response_model=Task)
def patch_task(task_id: int, updated_fields: TaskUpdate):

    for index, task in enumerate(TASK_DB):
        if task["id"] == task_id:
            update_data = updated_fields.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                task[key] = value                
            TASK_DB[index] = task
            return task
            
    raise HTTPException(status_code=404, detail="Tarea no encontrada para actualización parcial")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for index, task in enumerate(TASK_DB):
        if task["id"] == task_id:
            TASK_DB.pop(index)
            return
            
    raise HTTPException(status_code=404, detail="Tarea no encontrada para eliminar!!!")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)