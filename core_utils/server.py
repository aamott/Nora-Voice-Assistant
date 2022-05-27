################################
# Web Server
# https://fastapi.tiangolo.com/tutorial/first-steps/
################################
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/", StaticFiles(directory="server", html=True), name="site")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/settings")
async def read_user_me():
    return {"settings": "some settings"}