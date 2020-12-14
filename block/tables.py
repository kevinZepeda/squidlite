from sqlalchemy import MetaData
from session import engine
data = MetaData()

data.reflect(bind=engine)

users = data.tables['users']
urls = data.tables['urls']
block = data.tables['block']