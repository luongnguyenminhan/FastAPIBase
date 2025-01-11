from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import time
import os
from dotenv import load_dotenv  # type: ignore

load_dotenv()

Base = declarative_base()
max_retries = 5
retry_delay = 5

def create_engine_with_retry():
    for attempt in range(max_retries):
        try:
            engine = create_engine(
                url=os.getenv("SQLALCHEMY_DATABASE_URI"),
                pool_pre_ping=True,
                pool_recycle=3600,
                pool_size=5,
                max_overflow=10,
                pool_timeout=30,
                connect_args={
                    'connect_timeout': 60
                }
            )
            # Test connection
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print("Database connection successful!")
            return engine
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Database connection attempt {attempt + 1} failed, retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"Failed to connect to database after {max_retries} attempts")
                raise e

engine = create_engine_with_retry()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()