from fastapi import FastAPI, HTTPException,APIRouter,Header
from utils import create_token, decode_token,get_user
import dbhandler as dbhandler
from pydantic import BaseModel
from main import dbclient
import hashlib 
import os

router = APIRouter()
salt = os.getenv("SALT")

def hash_password(password):
    hashed_pass = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return salt + hashed_pass.hex()


class SignupRequest(BaseModel):
    email: str
    password: str
    username: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/auth/signup")
async def signup(data: SignupRequest):
    email = data.email
    password = data.password
    password = hash_password(password)
    username = data.username

    if dbhandler.add_user(dbclient, email, password, username):
        return {"status": "success", "token": create_token({"email": email})}
    raise HTTPException(status_code=400, detail="User already exists/Invalid data")

@router.post("/auth/login") 
async def login(data:LoginRequest):
    email = data.email
    password = data.password
    password = hash_password(password)

    user = dbhandler.get_user(dbclient, email)
    if user:
        if user.get("password") == password:
            return {"status": "success", "token": create_token({"email": email})}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.get("/auth/verify")
async def verify(Authorization: str = Header(None)):
    if Authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")    
    try:
        token = Authorization.split(" ")[1]
        user = get_user(token)
       
        if user:
            return {"status": "success"}
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")
    

