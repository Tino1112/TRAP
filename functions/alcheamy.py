from sqlalchemy.inspection import inspect

def db_records_to_dicts(db_records):
    dicts = []
    if not isinstance(db_records, list):
        db_records = [db_records]
    for record in db_records:
        if isinstance(record, tuple) and len(record) == 1:
            record = record[0]

        mapper = inspect(record).mapper
        record_dict = {column.key: getattr(record, column.key) for column in mapper.columns}

        dicts.append(record_dict)

    return dicts
