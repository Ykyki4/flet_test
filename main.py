from typing import Dict, Optional, List

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

app = FastAPI(title="In-memory CRUD example")

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class Item(ItemCreate):
    id: int

_db: Dict[int, Item] = {}
_next_id = 1

@app.post("/items/", response_model=Item, status_code=201)
def create_item(item: ItemCreate):
    global _next_id
    item_id = _next_id
    obj = Item(id=item_id, **item.dict())
    _db[item_id] = obj
    _next_id += 1
    return obj

@app.get("/items/", response_model=List[Item])
def list_items():
    return list(_db.values())

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    item = _db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemCreate):
    if item_id not in _db:
        raise HTTPException(status_code=404, detail="Item not found")
    updated = Item(id=item_id, **item.dict())
    _db[item_id] = updated
    return updated

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    if item_id not in _db:
        raise HTTPException(status_code=404, detail="Item not found")
    del _db[item_id]
    return Response(status_code=204)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
