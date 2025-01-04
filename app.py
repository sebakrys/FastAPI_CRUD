import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.sql import select
from databases import Database
from dotenv import load_dotenv

# Ładowanie zmiennych środowiskowych
load_dotenv()

# Konfiguracja bazy danych
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in environment variables")

database = Database(DATABASE_URL)
metadata = MetaData()

# Definicja tabeli użytkowników
users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
    Column("email", String(100), unique=False, nullable=False),
)

# Inicjalizacja bazy danych
engine = create_engine(DATABASE_URL)
metadata.create_all(engine)

# FastAPI aplikacja
app = FastAPI()


# Model Pydantic
class User(BaseModel):
    id: int
    name: str
    email: str


class UserCreate(BaseModel):
    name: str
    email: str


@app.on_event("startup")
async def startup():
    """Uruchomienie połączenia z bazą danych."""
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    """Zamknięcie połączenia z bazą danych."""
    await database.disconnect()


@app.get("/users", response_model=List[User])
async def get_users():
    """Pobiera wszystkich użytkowników z bazy danych."""
    query = select(users_table)
    results = await database.fetch_all(query)
    return results


@app.post("/users", response_model=User)
async def create_user(user: UserCreate):
    """Dodaje nowego użytkownika do bazy danych."""
    query = users_table.insert().values(name=user.name, email=user.email)
    user_id = await database.execute(query)
    return {"id": user_id, "name": user.name, "email": user.email}


@app.put("/users", response_model=User)
async def update_user(user: User):
    """Aktualizuje dane użytkownika w bazie danych."""
    found_user = await database.fetch_one(
        users_table.select()
        .where(users_table.c.id == user.id)
    )

    if not found_user:
        raise HTTPException(status_code=404, detail="User not found")

    query = (
        users_table.update()
        .where(users_table.c.id == user.id)
        .values(name=user.name, email=user.email)
    )
    await database.execute(query)

    updated_user = await database.fetch_one(
        users_table.select().where(users_table.c.id == user.id)
    )

    return updated_user


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """Usuwa użytkownika z bazy danych."""

    found_user = await database.fetch_one(
        users_table.select().where(users_table.c.id == user_id)
    )
    if not found_user:
        raise HTTPException(status_code=404, detail="User not found")

    query = users_table.delete().where(users_table.c.id == user_id)
    await database.execute(query)

    return {"message": "User deleted successfully"}
