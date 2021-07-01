import databases
import sqlalchemy
import os

DATABASE_URL = \
f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}/{os.environ['POSTGRES_DB']}"


database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL)