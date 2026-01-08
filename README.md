
# Trading API Wrapper - README

## Setup and Run Instructions

1. (Optional) Create a virtual environment:
   python -m venv .venv

2. Activate the virtual environment:
   - Windows: .venv\Scripts\activate
   - macOS/Linux: source .venv/bin/activate

3. Install dependencies:
   pip install -r requirements.txt

4. Start the FastAPI server:
   uvicorn app.main:app --reload

5. Open your browser and visit:
   http://127.0.0.1:8000/docs (for Swagger UI)

---


## Testing the API (with curl)

### 1. View Available Financial Instruments
```
  - List all executed trades for the user

**Sample Response:**
[
  {
    "symbol": "AAPL",
    "exchange": "NASDAQ",
    "instrumentType": "EQUITY",
    "lastTradedPrice": 180.0
  },
  ...
]

### 2. Place Buy/Sell Orders
**Market Order (Immediate Execution):**
```
### 4. Portfolio
- **GET /api/v1/portfolio**
  - Fetch current portfolio holdings
  - Response fields: symbol, quantity, averagePrice, currentValue
**Limit Order (Placed, not executed):**
```

---

## Assumptions Made
**Error (Missing price for LIMIT order):**
```
- Single hardcoded user (no authentication required)
- All data is stored in memory (no persistent database)
- Market orders are executed immediately; limit orders are placed
- No real market connectivity; all prices are simulated
**Sample Error Response:**
{
  "detail": "Price must be provided and > 0 for LIMIT orders."
}

### 3. Check Order Status
```
- No concurrency or multi-user support

Replace `{orderId}` with the ID returned from the order placement response.
**Sample Response:**
{
  "id": "...",
  "symbol": "AAPL",
  "orderType": "BUY",
  "orderStyle": "MARKET",
  "quantity": 5,
  "price": null,
  "status": "EXECUTED",
  "timestamp": "..."
}

### 4. View Executed Trades
```
---

**Sample Response:**
[
  {
    "id": "...",
    "orderId": "...",
    "symbol": "AAPL",
    "quantity": 5,
    "price": 180.0,
    "timestamp": "..."
  }
]

### 5. Fetch Basic Portfolio Holdings
```
## Sample API Usage

**Sample Response:**
[
  {
    "symbol": "AAPL",
    "quantity": 5,
    "averagePrice": 180.0,
    "currentValue": 900.0
  }
]

### 6. Error Handling Example (Invalid Order Quantity)
```
See interactive documentation and try requests at: http://127.0.0.1:8000/docs

Example: Place a market order

**Sample Error Response:**
{
  "detail": "Quantity must be greater than 0."
}

---

For more details and to interact with the API, use the Swagger UI at http://127.0.0.1:8000/docs
POST /api/v1/orders
{
  "symbol": "AAPL",
  "orderType": "BUY",
  "orderStyle": "MARKET",
  "quantity": 10
}

---

For more details, see the OpenAPI docs after running the server.
