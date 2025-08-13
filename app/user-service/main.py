from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String

# --- DB Setup ---
DATABASE_URL = "postgresql://dhiraj:g9T!r7wqLz@postgres:5432/chaos_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# --- Model ---
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

# --- Request Schema ---
class UserCreate(BaseModel):
    name: str
    email: str

# --- App Init ---
app = FastAPI()

# --- POST /users ---
@app.post("/users")
def create_user(user: UserCreate):
    db = SessionLocal()
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return {"id": new_user.id, "email": new_user.email}

# --- GET /users ---
@app.get("/users")
def get_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return [{"id": u.id, "name": u.name, "email": u.email} for u in users]
