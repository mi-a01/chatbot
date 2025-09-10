from fastapi import FastAPI, Query
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db import CallRecord
from config import DATABASE_URL

app = FastAPI()

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

@app.get("/search")
def search(keyword: str = Query(..., min_length=1)):
    session = SessionLocal()
    results = session.query(CallRecord).filter(CallRecord.content.contains(keyword)).all()
    session.close()
    return [{"summary": r.summary, "content": r.content} for r in results]

# http://127.0.0.1:8000/search?keyword=電話
