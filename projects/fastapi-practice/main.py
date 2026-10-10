# 一个FastAPI()实例。
import fastapi
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    list_name: str | None = None


items: dict[int, dict] = {}
next_id = 1
app = fastapi.FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/items")
def create_item(item: Item):
    global next_id
    new_id = next_id  # ① 先把这次要用的号抄一份出来
    data = item.model_dump() 
    data["id"] = new_id  
    items[new_id] = data   
    next_id += 1  
    return data

@app.get("/items")
def get_items():
    return list(items.values())