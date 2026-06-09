from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal, Base
from models import Monument

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow frontend (React) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add sample data
@app.post("/add-sample")
def add_sample(db: Session = Depends(get_db)):
    monument = Monument(
        name="Taj Mahal",
        location="Agra",
        description="Built by Shah Jahan in memory of Mumtaz Mahal",
        image_url="https://upload.wikimedia.org/wikipedia/commons/d/da/Taj-Mahal.jpg"
    )
    db.add(monument)
    db.commit()
    return {"message": "Sample added"}

# Get all monuments
@app.get("/monuments")
def get_monuments(db: Session = Depends(get_db)):
    return db.query(Monument).all()