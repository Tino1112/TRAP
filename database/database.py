import os
import hashlib
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Database:
    def __init__(self, dbname, logger, driver='psycopg2'):
        load_dotenv()
        if dbname is None:
            logger.error('Database name cannot be None')
            return

        con_string = 'postgresql+{driver}://{user}:{psw}@{host}:{port}/{db}'
        self.params = ['user', 'psw', 'host', 'port', 'db']
        params = {param: os.getenv(f'{dbname}_{param}') for param in self.params}
        params['driver'] = driver
        self.con_string = con_string.format(**params)
        self.engine = create_engine(self.con_string)

    def start_session(self):
        return sessionmaker(self.engine)()

    def bulk_insert(self, insert_data, db_table, session):
        insert_data = self.insert_data_check(insert_data)
        for data in insert_data:
            new_record = db_table(**data)
            session.add(new_record)
        session.commit()


    def merge(self, insert_data, db_table, filters, session, keys_order, unique_value, archive_col='archived', stats=False):
        # for stats
        inserted = 0
        updated = 0
        unchanged = 0
        insert_data = self.insert_data_check(insert_data)

        # hash insert data for comparing to db data
        insert_data = self.hash_insert_data(insert_data, keys_order)
        db_objs = session.query(db_table).filter(filters).all()
        db_map = {getattr(obj, unique_value): obj for obj in db_objs}

        for data in insert_data:
            new_record = db_table(**data)
            db_record = db_map.get(data[unique_value])
            if not db_record:
                session.add(new_record)
                inserted += 1
                continue
            if db_record.sha == data['sha']:
                unchanged += 1
                continue
            setattr(db_record, archive_col, datetime.now())
            session.add(new_record)
            updated += 1

        session.commit()
        if stats:
            return Stats(inserted, updated, unchanged)

    def hash_insert_data(self, insert_data, keys_order):
        new_insert_data = []
        for data in insert_data:
            missing = [k for k in keys_order if k not in data]
            if missing:
                raise KeyError(f"Missing keys for hashing: {missing}")
            data = {k: data[k] for k in keys_order if k in data}
            hash_data = str(list(data.values())).encode()
            values_hash = hashlib.sha3_256(hash_data).hexdigest()
            data['sha'] = values_hash
            new_insert_data.append(data)

        return new_insert_data

    def insert_data_check(self, insert_data):
        if not isinstance(insert_data, list) or not all(isinstance(item, dict) for item in insert_data):
            if isinstance(insert_data, dict):
                return [insert_data]
            else:
                raise TypeError("insert_data must be a list of dictionaries")
        return insert_data

class Stats:
    def __init__(self, inserted=0, updated=0, unchanged=0):
        self.inserted = inserted
        self.updated = updated
        self.unchanged = unchanged

















