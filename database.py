from sqlalchemy import create_engine, Table, MetaData, update, select, desc, or_, Column, Integer, \
    Sequence, asc
from sqlalchemy.orm import sessionmaker
import psycopg2
from sqlalchemy.dialects.postgresql import psycopg2
import os
import encrypt

engine = create_engine('postgresql://ohxbpooneyznrg:3971f8b9f0d67ac14629551339d9ba793ad8da29be40656290a923577b204b47@ec'
                       '2-23-20-211-19.compute-1.amazonaws.com:5432/dcj5ar95ejloos')
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()
conn = engine.connect()


def load_table(table_name):
    table = Table(table_name, metadata, autoload=True, autoload_with=engine)
    return table


def read_rows(table_name):
    query = session.query(load_table(table_name))
    data = []
    for row in query:
        data += [row]
    return data


def get_account(row_id):
    account = session.query(load_table('AccountChain')).filter_by(User_ID=row_id).first()
    return account


def change_balance(row_id, new_balance):
    table = load_table('AccountChain')
    stmt = update(table).where(table.c.User_ID == row_id).values(Balance=new_balance)
    conn.execute(stmt)


def add_row(table_name, new_row):
    table = load_table(table_name)
    new_id = 0
    if table_name == 'SessionChain':
        new_id = conn.execute("SELECT nextval('session_id_seq')").scalar()
    elif table_name == 'TransactionChain':
        new_id = conn.execute("SELECT nextval('transaction_id_seq')").scalar()
    elif table_name == 'AccountChain':
        new_id = conn.execute("SELECT nextval('user_id_seq')").scalar()
    elif table_name == 'DepositChain':
        new_id = conn.execute("SELECT nextval('deposit_id_seq')").scalar()
    new_row[0] = new_id
    stmt = table.insert().values(new_row)
    conn.execute(stmt)
    return new_id


def get_latest_key():
    table = load_table('TransactionChain')
    last_row = session.query(table).order_by(desc(table.c['Transaction_ID'])).first()
    return last_row['New_Hash']


def get_transactions(id_num):
    table = load_table('TransactionChain')
    results = session.query(table).filter(or_(table.c['Sender_ID'].like(id_num),
                                              table.c['Recipient_ID'].like(id_num))).all()
    return results


def get_user_ids():
    table = load_table('AccountChain')
    results = [result[0] for result in session.query(table.c['User_ID']).all()]
    return results


def get_total_deposits():
    table = load_table('DepositChain')
    result = sum(float(encrypt.decrypt_string(deposit[0])) for deposit in session.query(table.c['Amount']).all())
    return result
