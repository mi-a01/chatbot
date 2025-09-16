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
    session = SessionLocal()
    results = session.query(CallRecord).filter(CallRecord.content.contains(keyword)).all()
    session.close()
    return [{"summary": r.summary, "content": r.content} for r in results]

if __name__ == "__main__":
    import main  # ← DB処理を実行
    uvicorn.run(app, host="0.0.0.0", port=10000)

# https://chatbot-o87s.onrender.com/search?keyword=%E9%9B%BB%E8%A9%B1
