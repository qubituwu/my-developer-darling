from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine
from backend import models, crud, schemas


# Initialize the FastAPI app
app = FastAPI()

# Example request model for generating images
class GenerateRequest(BaseModel):
    model_type: str  # "gan" or "diffusion"
    prompt: str = None  # Optional, for text-to-image models
    seed: int = None

# Dependency for getting the database session
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

# Image generation endpoint
@app.post("/generate")
async def generate_image(req: GenerateRequest):
    if req.model_type == "gan":
        return {"status": "Running GAN model...", "prompt": req.prompt, "seed": req.seed}
    elif req.model_type == "diffusion":
        return {"status": "Running Diffusion model...", "prompt": req.prompt, "seed": req.seed}
    else:
        return {"error": "Invalid model_type. Use 'gan' or 'diffusion'."}

@app.post("/items/")
async def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.create_item(db=db, item=item)
    return db_item

# Get all items from the database
@app.get("/items/")
async def read_items(db: Session = Depends(get_db)):
    items = crud.get_items(db=db)
    return items

# Get a specific item by ID
@app.get("/items/{item_id}")
async def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
