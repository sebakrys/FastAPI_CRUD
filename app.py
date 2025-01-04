from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str

users: List[User] = []

@app.get("/users", response_model=List[User])
def get_users():
    return users

@app.post("/users", response_model=User)
def create_user(user: User):
    users.append(user)
    return user

@app.put("/users", response_model=User)
def update_user(user: User):
    for index, saved_user in enumerate(users):
        if(saved_user.id==user.id):
            users[index] = user
            return users[index]
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    global users
    users = [user for user in users if user.id != user_id]
    return {"message": "User deleted"}
