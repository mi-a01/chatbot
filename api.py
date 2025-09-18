from fastapi import FastAPI, Query
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db import CallRecord
from config import DATABASE_URL
import uvicorn


app = FastAPI()

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

@app.get("/search")
def search(keyword: str = Query(..., min_length=1)):
    if not keyword:  # キーワードなしなら空配列
        return {"records": []}
        
    session = SessionLocal()
    results = session.query(CallRecord).filter(CallRecord.content.contains(keyword)).all()
    session.close()
    return [{"summary": r.summary, "content": r.content} for r in results]

# https://chatbot-o87s.onrender.com/search?keyword=%E9%9B%BB%E8%A9%B1

# ここから Dify用 retrieval API
@app.get("/retrieval")
def retrieval(keyword: str = Query(None, description="検索キーワード")):
    if not keyword:  # キーワードなしなら空配列
        return {"records": []}

    session = SessionLocal()
    results = session.query(CallRecord).filter(CallRecord.content.contains(keyword)).all()
    session.close()

    records = []
    for i, r in enumerate(results):
        records.append({
            "id": str(i),
            "title": r.summary or "",
            "content": r.content or "",
            "metadata": {"source": "render-db"}
        })

    return {"records": records}
