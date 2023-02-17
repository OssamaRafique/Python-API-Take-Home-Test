
import sqlalchemy.orm
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine



Base = sqlalchemy.orm.declarative_base()


# Define the database connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./db/test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

