from sqlalchemy import Column, Integer, String, MetaData, Table, inspect

metadata = MetaData()

def create_reply_log_table(engine):
    inspector = inspect(engine)
    if inspector.get_table_names('reply_log'):
        pass
    else:
        reply_log = Table(
            'reply_log', metadata,
            Column('id', Integer, primary_key=True),
            Column('question', String(255), nullable=False),
            Column('answer', String(255), nullable=False),
            Column('bot_type', String(10), nullable=False),
        )        
        metadata.create_all(engine)