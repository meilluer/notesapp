
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class NoteIn(BaseModel):
    title: str
    content: Optional[str] = None
    tags: Optional[List[str]] = []
_notes = {}
_next = 1

@app.post("/notes", status_code=201)
def create_note(payload: NoteIn):
    global _next
    note = payload.dict()
    note_id = _next; _next += 1
    note_out = {"id": note_id, **note}
    _notes[note_id] = note_out
    return note_out

@app.get("/notes")
def list_notes():
    return list(_notes.values())

@app.get("/notes/{note_id}")
def get_note(note_id: int):
    n = _notes.get(note_id)
    if not n: raise HTTPException(404, "not found")
    return n
