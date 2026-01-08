from fastapi import APIRouter
from typing import List
from app.models import PortfolioItem, OrderStatus, OrderType
from app.orders import orders_db

router = APIRouter(prefix="/api/v1/portfolio", tags=["Portfolio"])

@router.get("/", response_model=List[PortfolioItem])
def get_portfolio():
    pf = {}
    for o in orders_db.values():
        if o.status == "EXECUTED" or o.status == OrderStatus.EXECUTED:
            if o.symbol not in pf:
                pf[o.symbol] = {"quantity": 0, "total": 0.0}
            if o.orderType == "BUY" or o.orderType == OrderType.BUY:
                pf[o.symbol]["quantity"] += o.quantity
                pf[o.symbol]["total"] += (o.price or 0.0) * o.quantity
            elif o.orderType == "SELL" or o.orderType == OrderType.SELL:
                pf[o.symbol]["quantity"] -= o.quantity
                pf[o.symbol]["total"] -= (o.price or 0.0) * o.quantity
    res = []
    for sym, d in pf.items():
        qty = d["quantity"]
        avg = (d["total"] / qty) if qty != 0 else 0.0
        val = qty * avg
        res.append(PortfolioItem(symbol=sym, quantity=qty, averagePrice=avg, currentValue=val))
    return res
