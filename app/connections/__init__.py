from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.services.db.create_table import create_reply_log_table
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
        
    def close(self):
        self.engine.dispose()
        self.session.close()
        print("---- postgres closed ----")
        
postgres = PostgresClient()