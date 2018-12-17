from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

host = '127.0.0.1'
port = '3306'
database = 'tudo28'
user = 'admin'
password = 'Root110qwe'

db_url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    user,password,host,port,database
)

engine = create_engine(db_url)

# if __name__ == '__main__':
#     connection = engine.connect()
#     result = connection.execute('select 1')
#     print(result.fetchone())

DBSession = sessionmaker(bind=engine)
Base = declarative_base(engine)