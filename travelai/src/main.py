from fastapi import FastAPI
from travelai.src.api.ledgers.router import router as ledger_router
from travelai.src.core.config import SQLALCHEMY_DATABASE_URI
from sqlalchemy import create_engine

app = FastAPI()
app.include_router(ledger_router, prefix="/ledger", tags=["ledger"])

engine = create_engine(SQLALCHEMY_DATABASE_URI)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
