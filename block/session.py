from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///squidlite.db')
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = Session()
