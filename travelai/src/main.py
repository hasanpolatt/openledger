from fastapi import FastAPI
from sqlalchemy import create_engine

from travelai.src.api.ledgers.router import router as ledger_router
from travelai.src.core.config import SQLALCHEMY_DATABASE_URI

app = FastAPI(
    title="TravelAI API",
    description="API for TravelAI service ledger operations",
    version="1.0.0",
)

# Include routers
app.include_router(ledger_router)

engine = create_engine(SQLALCHEMY_DATABASE_URI)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "travelai.src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
