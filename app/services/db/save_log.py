from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from app.connections import postgres

# 모델 생성
Base = declarative_base()

class ReplyLog(Base):
    __tablename__ = 'reply_log'
    id = Column(Integer, primary_key=True)
    question = Column(String(255), nullable=False)
    answer = Column(String(255), nullable=False)
    bot_type = Column(String(255), nullable=False)
    
def save_reply_log(question, answer, bot_type):
    try:
        reply_log = ReplyLog(question=question, answer=answer, bot_type=bot_type)
        postgres.session.add(reply_log)
        postgres.session.commit()
    except Exception as e:
        print(e)
        postgres.session.rollback()
        raise e
    
if __name__ == "__main__":
    postgres.connect()
    save_reply_log("안녕", "안녕하세요", "1")
    postgres.close()