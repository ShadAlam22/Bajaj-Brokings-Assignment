from fastapi import APIRouter
from typing import List
from app.models import Instrument

router = APIRouter(prefix="/api/v1/instruments", tags=["Instruments"])
instruments_db = [
    Instrument(symbol="AAPL", exchange="NASDAQ", instrumentType="EQUITY", lastTradedPrice=180.0),
    Instrument(symbol="GOOGL", exchange="NASDAQ", instrumentType="EQUITY", lastTradedPrice=2700.0),
    Instrument(symbol="NIFTY21JULFUT", exchange="NSE", instrumentType="FUTURE", lastTradedPrice=18000.0)
]

@router.get("/", response_model=List[Instrument])
def get_instruments():
    return instruments_db
