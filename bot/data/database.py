from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os
load_dotenv('./.env')

config = os.environ

DB_USERNAME = config["DATABASE_USERNAME"]
DB_PASSWORD = config["DATABASE_PASS"]
DB_ADRESS = config["DATABASE_ADRESS"]
DB_NAME = config["DATABASE_NAME"]

engine = create_engine("postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_ADRESS}/{DB_NAME}", echo=True)

class Base(DeclarativeBase): pass

Sessionlocal = sessionmaker(bind=engine)
