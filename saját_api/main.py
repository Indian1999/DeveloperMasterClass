#pip install fastapi uvicorn
#uvicorn main:app --reload (szerver futtatása)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    person: str = None
    description: str = None
    is_done: bool = False

tasks = []
items = []
names = ["András", "Béla", "Cecil", "Dénes", "Elemér", "Ferenc", "Géza"]

@app.get("/")
def root():
    return {"Hello": "World"}

@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task)
    return task

@app.get("/tasks", response_model=list[Task])
def list_tasks(limit: int = 3):
    return tasks[:limit]

@app.get("/names")
def get_names():
    return names

@app.post("/items")
def create_item(item: str):
    items.append(item)
    return item

@app.get("/items/{item_id}")
def get_item(item_id: int) -> str:
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item index does not exist")
    else:
        return items[item_id]