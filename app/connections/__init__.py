from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.create import create_reply_log_table
from app.db.insert import insert_answer
from app.config import settings

HOST = settings.DB_HOST
PORT = settings.DB_PORT
PW = settings.DB_PASSWORD
USER = settings.DB_USER
DB = settings.DB_NAME

class PostgresClient:
    def __init__(self):
        self.engine = None
        self.session = None
        
    def connect(self):
        self.engine = create_engine(f'postgresql://{USER}:{PW}@{HOST}:{PORT}/{DB}')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        print("---- postgres connected ----")
        
    def prepare(self):
        create_reply_log_table(self.engine)
        insert_answer(self.engine)
        
    def close(self):
        self.engine.dispose()
        self.session.close()
        print("---- postgres closed ----")
        
postgres = PostgresClient()