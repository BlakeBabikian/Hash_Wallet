from sqlalchemy import create_engine, Table, MetaData, update, select
from sqlalchemy.orm import sessionmaker
import os

# create a connection to the database
os.environ['SQLALCHEMY_WARN_20']='2'
engine = create_engine('sqlite:///data.db')

# create a session
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()

# define the table you want to iterate through
table = Table('AccountChain', metadata, autoload=True, autoload_with=engine)
conn = engine.connect()

# Change Data in an existed row
"""stmt = update(table).where(table.c.User_ID == 2).values(Balance = "200")
conn = engine.connect()
conn.execute(stmt)"""

# Add a new row
"""stmt = select([table]).select_from(table).alias('count')
result = conn.execute(stmt).scalar()
next_id = result + 1
new_row = [None,"Test3", "Name4", "Blah5", "10.0"]
stmt = Table.insert(table).values(new_row)
conn.execute(stmt)"""

# Get row based on id - primary
"""account = session.query(table).filter_by(User_ID=1).first()
print(account[1])"""


query = session.query(table)
print(type(query))
print(query)
# iterate through the results
for row in query:
    print(row)




