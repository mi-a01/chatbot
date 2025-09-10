from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class CallRecord(Base):
    __tablename__ = "calls"
    id = Column(Integer, primary_key=True, index=True)
    summary = Column(Text)   # Q列
    content = Column(Text)   # R列

def init_db():
    Base.metadata.create_all(bind=engine)

def save_to_db(records):
    session = SessionLocal()
    for rec in records:
        exists = session.query(CallRecord).filter_by(content=rec["content"]).first()
        if not exists:  # 重複チェック
            session.add(CallRecord(summary=rec["summary"], content=rec["content"]))
    session.commit()
    session.close()
