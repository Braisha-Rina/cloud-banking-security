from fastapi import FastAPI
from pydantic import BaseModel, Field
class Account(BaseModel):
    account_id: str
    currency: str
    balance: float
app = FastAPI()
accounts = []
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