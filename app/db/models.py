from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Answer(Base):
    __tablename__ = 'answer'
    id = Column(Integer, primary_key=True)
    user = Column(String(255), nullable=False)
    system = Column(String(512), nullable=False)
    sentiment = Column(String(32))

class ReplyLog(Base):
    __tablename__ = 'reply_log'
    id = Column(Integer, primary_key=True)
    question = Column(String(255), nullable=False)
    answer = Column(String(255), nullable=False)
    bot_type = Column(String(10), nullable=False)