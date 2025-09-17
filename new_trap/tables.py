from datetime import datetime
import logging
from sqlalchemy import *
from sqlalchemy.orm import declarative_base
from database.database import Database

pstg_schema = 'tt'
Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': pstg_schema}

    id = Column(Integer, primary_key=True, autoincrement=True)
    sha = Column(VARCHAR(100))

    name = Column(VARCHAR(100))
    surname = Column(VARCHAR(100))
    username = Column(VARCHAR(20), nullable=False, unique=True)
    password = Column(VARCHAR(20), nullable=False)
    admin = Column(Boolean, nullable=False, default=False)

    date_created = Column(DateTime, default=datetime.now)
    archived = Column(DateTime)

class Logs(Base):
    __tablename__ = 'logs'
    __table_args__ = {'schema': pstg_schema}

    id = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(VARCHAR(20), nullable=False)
    func_name = Column(VARCHAR(20), nullable=False)
    params = Column(TEXT)

    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    runtime = Column(Float, nullable=False)

    error_msg = Column(TEXT)

    created_at = Column(DateTime, default=datetime.now)

def create_tables():
    Base.metadata.drop_all(database.engine)
    Base.metadata.create_all(database.engine)

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    database = Database('pstg', logger)

    create_tables()

