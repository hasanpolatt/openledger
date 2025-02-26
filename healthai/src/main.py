from fastapi import FastAPI
from sqlalchemy import create_engine

from healthai.src.api.ledgers.router import router as ledger_router
from healthai.src.core.config import SQLALCHEMY_DATABASE_URI

app = FastAPI(
    title="HealthAI API",
    description="API for HealthAI service ledger operations",
    version="1.0.0",
)

app.include_router(ledger_router)

engine = create_engine(SQLALCHEMY_DATABASE_URI)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("healthai.src.main:app", host="0.0.0.0", port=8005, reload=True)
