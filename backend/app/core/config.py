from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Project"
    API_V1_STR: str = "/api/v1"
    SQLALCHEMY_DATABASE_URI: str = "mysql+mysqlconnector://user:password@localhost:3306/dbname"

    class Config:
        case_sensitive = True

settings = Settings()
