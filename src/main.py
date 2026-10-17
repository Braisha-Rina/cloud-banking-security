from fastapi import FastAPI
from pydantic import BaseModel, Field
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
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
    username: str
    password_hash: str
class UserRegistration(BaseModel):
    username: str = Field(min_length=3, max_length=30, strip_whitespace=True)
    password: str = Field(min_length=8, max_length=128)