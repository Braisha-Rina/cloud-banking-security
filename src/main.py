from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from uuid import uuid4
class Account(BaseModel):
    account_id: str
    currency: str
    balance: float
app = FastAPI()
accounts = []
users = []
@app.get("/")
def root1() :
    return {"message":"Cloud Banking Security Platform API is running"}
@app.post("/account")
def create_account(account: Account):
    account_data = account.model_dump()
    accounts.append(account_data)
    return account_data
@app.get("/account")
def get_accounts():
    return accounts
password_hash = PasswordHasher()
def hash_password(password: str):#str
    return password_hash.hash(password)
def verify_password(password: str, hashed_password: str) :#bool
    try:
        return password_hash.verify(hashed_password, password)
    except VerifyMismatchError:
        return False
class User(BaseModel):
    user_id: str
    email: str
    password_hash: str
class UserRegistration(BaseModel):
    email:EmailStr
    password: str = Field(min_length=8, max_length=128)
@app.post("/register")
def register_user(user: UserRegistration):
    for existing_user in users:
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=409,
                detail="Email already registered"
    )
    new_user = User(
        user_id=str(uuid4()),
        email=user.email,
        password_hash=hash_password(user.password)
    )
    users.append(new_user.model_dump())
    return {
        "user_id": new_user.user_id,
        "email": new_user.email,
        "message": "User registered successfully"
    }