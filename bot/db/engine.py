from sqlalchemy import create_engine
from models import Base


engine = create_engine('sqlite:///sqlite.db', echo=True)
Base.metadata.create_all(engine)
