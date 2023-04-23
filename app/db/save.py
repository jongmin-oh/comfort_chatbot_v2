from app.connections import postgres
from app.db.models import ReplyLog


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
