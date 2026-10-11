from fastapi import FastAPI
from pydantic import BaseModel, Field
app = FastAPI()
@app.get("/")
def root1() :
    return {"message":"Cloud Banking Security Platform API is running"}
class Account(BaseModel):
    account_id: str
    currency: str
    balance: float
@app.post("/account")
def create_account(account: Account):
        return account.model_dump()