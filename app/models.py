from pydantic import BaseModel
from typing import Optional
from enum import Enum

class InstrumentType(str, Enum):
    EQUITY = "EQUITY"
    ETF = "ETF"
    FUTURE = "FUTURE"
    OPTION = "OPTION"

class Instrument(BaseModel):
    symbol: str
    exchange: str
    instrumentType: InstrumentType
    lastTradedPrice: float

class OrderType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderStyle(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"

class OrderStatus(str, Enum):
    NEW = "NEW"
    PLACED = "PLACED"
    EXECUTED = "EXECUTED"
    CANCELLED = "CANCELLED"

class Order(BaseModel):
    id: str
    symbol: str
    orderType: OrderType
    orderStyle: OrderStyle
    quantity: int
    price: Optional[float] = None
    status: OrderStatus
    timestamp: str

class Trade(BaseModel):
    id: str
    orderId: str
    symbol: str
    quantity: int
    price: float
    timestamp: str

class PortfolioItem(BaseModel):
    symbol: str
    quantity: int
    averagePrice: float
    currentValue: float
