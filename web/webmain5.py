from fastapi import FastAPI, status, Body, HTTPException, Path, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
from typing import Annotated


app = FastAPI()
templates = Jinja2Templates(directory="templates")

Users = []

class User(BaseModel):
    id: int = None
    username: str = None
    age: int = None


@app.get("/")
async def welcome_for_users() -> str:
    return "Welcome"

@app.get("/users")
async def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": Users})


@app.get(path="/user/{user_id}")
def get_user(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse("users.html", {"request": request, "user": Users[user_id-1]})
    except:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")


@app.post("/user/{username}/{age}")
async def create_user(user: User) -> str:
    user.id = len(Users)+1
    Users.append(user)
    return f"The user {len(Users)} is registered"


@app.put("/user/{user_id}/{username}/{age}")
async def update_message(user_id: int, user: User) -> str:
    try:
        edit_user = Users[user_id-1]
        user.id = user_id
        edit_user.username = user
        return f"The user {user_id} is updated"
    except:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")


@app.delete("/user/{user_id}")
async def delete_message(user_id: int) -> str:
    try:
        Users.pop(user_id)
        return f"User with {user_id} was deleted"
    except:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")


