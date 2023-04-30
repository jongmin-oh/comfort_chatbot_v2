from sqlalchemy import inspect
from app.db.models import Answer, ReplyLog


def is_exist_table(engine, table_name) -> bool:
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()


def create_answer_table(engine):
    if not is_exist_table(engine, "answer"):
        Answer.__table__.create(engine)


def create_reply_log_table(engine):
    if not is_exist_table(engine, "reply_log"):
        ReplyLog.__table__.create(engine)
