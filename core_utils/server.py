################################
# Web Server
# https://fastapi.tiangolo.com/tutorial/first-steps/
# Starting and stopping the server: 
#       https://stackoverflow.com/questions/61577643/python-how-to-use-fastapi-and-uvicorn-run-without-blocking-the-thread
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