from fastapi import APIRouter, HTTPException
from app.models import Order, OrderType, OrderStyle, OrderStatus, Trade
from datetime import datetime
import uuid
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])
orders_db = {}

class OrderRequest(BaseModel):
    symbol: str
    orderType: OrderType
    orderStyle: OrderStyle
    quantity: int
    price: float = None
    class Config:
        schema_extra = {
            "example": {
                "symbol": "AAPL",
                "orderType": "BUY",
                "orderStyle": "MARKET",
                "quantity": 10,
                "price": 180.0
            }
        }

@router.post("/", response_model=Order)
def place_order(order: OrderRequest):
    if order.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0.")
    if order.orderStyle == OrderStyle.LIMIT and (order.price is None or order.price <= 0):
        raise HTTPException(status_code=400, detail="Price must be provided and > 0 for LIMIT orders.")
    order_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    status = OrderStatus.EXECUTED if order.orderStyle == OrderStyle.MARKET else OrderStatus.PLACED
    exec_price = order.price
    if status == OrderStatus.EXECUTED and (exec_price is None or exec_price == 0.0):
        from app.instruments import instruments_db
        instrument = next((i for i in instruments_db if i.symbol == order.symbol), None)
        if instrument:
            exec_price = instrument.lastTradedPrice
        else:
            exec_price = 0.0
    new_order = Order(
        id=order_id,
        symbol=order.symbol,
        orderType=order.orderType,
        orderStyle=order.orderStyle,
        quantity=order.quantity,
        price=exec_price,
        status=status,
        timestamp=now
    )
    orders_db[order_id] = new_order
    if status == OrderStatus.EXECUTED:
        from app.trades import trades_db
        trades_db.append(Trade(
            id=order_id,
            orderId=order_id,
            symbol=order.symbol,
            quantity=order.quantity,
            price=exec_price,
            timestamp=now
        ))
    return new_order

@router.get("/{order_id}", response_model=Order)
def get_order(order_id: str):
    order = orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    return order
