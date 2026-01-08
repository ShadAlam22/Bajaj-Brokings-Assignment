
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.instruments import router as instruments_router
from app.orders import router as orders_router
from app.trades import router as trades_router
from app.portfolio import router as portfolio_router

import logging
logging.basicConfig()
log = logging.getLogger()

app = FastAPI()

@app.exception_handler(Exception)
async def err_handler(request: Request, exc: Exception):
    print("Error happened:", exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

app.include_router(instruments_router)
app.include_router(orders_router)
app.include_router(trades_router)
app.include_router(portfolio_router)

@app.get("/")
def home():
    print("Root endpoint called")
    return {"message": "Trading API is running"}
