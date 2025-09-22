from datetime import datetime
import logging
from sqlalchemy import *
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import declarative_base
from database.database import Database

pstg_schema = 'internet_testing'
Base = declarative_base()

class Tests(Base):
    __tablename__ = 'tests'
    __table_args__ = ({'schema': pstg_schema})
    id = Column(Integer, primary_key=True)

    date = Column(DateTime, default=datetime.now)
    download_speed = Column(Float)
    upload_speed = Column(Float)
    ping = Column(Float)

def create_tables():
    Base.metadata.drop_all(database.engine)
    Base.metadata.create_all(database.engine)

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    database = Database('pstg', logger)

    create_tables()