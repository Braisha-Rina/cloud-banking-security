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
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
@app.post("/login")
def login_user(user: UserLogin):
    for existing_user in users:
        if existing_user["email"] == user.email:
            if verify_password(
                user.password,
                existing_user["password_hash"]
            ):
                return {
                    "message": "Login successful",
                    "user_id": existing_user["user_id"],
                    "email": existing_user["email"]
                }

            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

    raise HTTPException(
        status_code=401,
        detail="Invalid email or password"
    )
