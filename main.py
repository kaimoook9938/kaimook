from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

words_db = []

class Word(BaseModel):
    id: int
    word: str
    meaning: str

@app.get("/")
def serve_home():
    return FileResponse("static/index.html")

@app.get("/words")
def get_words():
    return sorted(words_db, key=lambda w: w.word)

@app.post("/words")
def add_word(word: Word):
    for w in words_db:
        if w.id == word.id:
            raise HTTPException(status_code=400, detail="ID นี้มีอยู่แล้ว")
    words_db.append(word)
    return {"message": "เพิ่มคำศัพท์แล้วจ้า"}

@app.delete("/words/{word_id}")
def delete_word(word_id: int):
    for w in words_db:
        if w.id == word_id:
            words_db.remove(w)
            return {"message": "ลบคำศัพท์แล้วจ้า"}
    raise HTTPException(status_code=404, detail="ไม่พบคำนั้น")
