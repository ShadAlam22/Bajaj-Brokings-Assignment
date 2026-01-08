from fastapi import APIRouter
from typing import List
from app.models import Trade

router = APIRouter(prefix="/api/v1/trades", tags=["Trades"])
trades_db = []

@router.get("/", response_model=List[Trade])
def get_trades():
    return trades_db
