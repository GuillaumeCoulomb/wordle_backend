from fastapi import FastAPI, Cookie, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from uuid import uuid4
import random

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True)
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


def chose_random_word(file):
    with open(file, 'r') as f:
        words = f.readlines()
    words = [mot.strip() for mot in words]  
    return random.choice(words)


file= 'word_list.txt'
SECRET_WORD = chose_random_word(file)


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

@app.post("/guess")
async def guess(word: str = Query(...), cookie_id: str = Cookie(alias="id")):
    if cookie_id not in user_ids:
        return {"status": "ignored"}
    word = word.upper()
    result = evaluate_word(word, SECRET_WORD)
    guesses.append((cookie_id, word, result))
    return {"status": "ok", "result": result}

@app.get("/state")
async def state():
    return {"guesses": guesses}

def evaluate_word(guess, secret):
    result = []
    for i in range(len(secret)):
        if guess[i] == secret[i]:
            result.append("green")
        elif guess[i] in secret:
            result.append("yellow")
        else:
            result.append("gray")
    return result
