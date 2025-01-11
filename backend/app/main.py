from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import API_V1_STR, PROJECT_NAME
from app.api.api_v1.api import api_router
from app.db.base import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text

app = FastAPI(title=PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test-db")
async def test_db(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1 as test"))
        return {"status": "success", "message": "Database connection successful", "result": result.first()[0]}
    except Exception as e:
        return {"status": "error", "message": f"Database connection failed: {str(e)}"}

app.include_router(api_router, prefix=API_V1_STR)
