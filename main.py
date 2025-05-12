from fastapi import FastAPI, Cookie, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from uuid import uuid4

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True)
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

SECRET_WORD = "MINES"
user_ids = set()
guesses = []

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

@app.get("/preinit")
async def preinit():
    user_id = str(uuid4())
    user_ids.add(user_id)
    res = JSONResponse({"status": "ok"})
    res.set_cookie("id", user_id, samesite="none", secure=True)
    return res

@app.get("/init")
async def init(cookie_id: str = Cookie(alias="id")):
    if cookie_id not in user_ids:
        return {"error": "invalid id"}
    return {"guesses": guesses}
