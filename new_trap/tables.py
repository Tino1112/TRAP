from datetime import datetime
import logging
from sqlalchemy import *
from sqlalchemy.dialects.postgresql import BYTEA
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

    date_created = Column(DateTime, default=datetime.now)

class Workers(Base):
    __tablename__ = "workers"
    __table_args__ = {"schema": pstg_schema}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, Sequence("worker_user_id_seq", schema=pstg_schema), unique=True, nullable=False)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    vat_number = Column(String(11), unique=True, nullable=False)

    date_created = Column(DateTime, default=datetime.now)
    archived = Column(DateTime)

class WorkersBasicInfo(Base):
    __tablename__ = "workers_basic_info"
    __table_args__ = {"schema": pstg_schema}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, nullable=False)

    passport_number = Column(String(20))
    id_number = Column(String(20))
    date_of_birth = Column(Date)
    place_of_birth = Column(String(100))
    residence = Column(String(200))
    temporary_residence = Column(String(200))
    contact_info = Column(String(50))

    date_created = Column(DateTime, default=datetime.now)
    archived = Column(DateTime)

class WorkerDetails(Base):
    __tablename__ = "workers_details"
    __table_args__ = {"schema": pstg_schema}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, nullable=False)

    police_station = Column(String(200))
    application_date = Column(Date)
    hzz_date = Column(Date)
    permit_date = Column(Date)
    permit_expiry_date = Column(Date)
    visa_date = Column(Date)
    arrival_date = Column(Date)
    medical_date = Column(Date)
    id_date = Column(Date)
    id_expiry_date = Column(Date)
    registration_date = Column(Date)
    reference_date = Column(Date)
    reference_number = Column(String(100))

    created_at = Column(DateTime, default=datetime.utcnow)
    archived = Column(DateTime)

class WorkHistory(Base):
    __tablename__ = "work_history"
    __table_args__ = {"schema": pstg_schema}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, nullable=False)

    companyzh = Column(VARCHAR(150))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    work_hours = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)
    archived = Column(DateTime)

class WorkersDocuments(Base):
    __tablename__ = "workers_documents"
    __table_args__ = {"schema": pstg_schema}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, nullable=False)

    file_name = Column(VARCHAR(100))
    description = Column(VARCHAR(100))
    content = Column(BYTEA, nullable=False)

    created_at = Column(DateTime, default=datetime.now)
    archived = Column(DateTime)

class Documents(Base):
    __tablename__ = "documents"
    __table_args__ = {"schema": pstg_schema}

    id = Column(Integer, primary_key=True, autoincrement=True)

    file_name = Column(VARCHAR(100))
    description = Column(VARCHAR(100))
    content = Column(BYTEA, nullable=False)

    created_at = Column(DateTime, default=datetime.now)
    archived = Column(DateTime)

def create_tables():
    Base.metadata.drop_all(database.engine)
    Base.metadata.create_all(database.engine)

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    database = Database('pstg', logger)

    create_tables()

