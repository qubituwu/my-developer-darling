from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine
from backend import models, crud, schemas
from backend.routers import ai_router

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Health check
@app.get("/")
async def root():
    return {"message": "haiiii, My Developer Darling API is live :3"}

# Items CRUD
@app.post("/items/")
async def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)
    
@app.get("/items/")
async def read_items(db: Session = Depends(get_db)):
    return crud.get_items(db=db)

@app.get("/items/{item_id}")
async def read_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db=db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Include AI routes
app.include_router(ai_router.router, prefix="/ai", tags=["AI"])
