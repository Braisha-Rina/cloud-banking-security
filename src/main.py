from fastapi import FastAPI

app1 = FastAPI()
@app1.get("/")
def root() :
    return {"message":"Cloud Banking Security Platform API is running"}
